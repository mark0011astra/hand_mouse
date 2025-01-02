import cv2
import mediapipe as mp
import numpy as np
import time
import win32api
import win32con
from filterpy.kalman import KalmanFilter

# デバッグモード (True: デバッグ情報を出力, False: 出力しない)
DEBUG = False

# ハンドトラッキングの初期化
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# カルマンフィルタの初期化
kf = KalmanFilter(dim_x=4, dim_z=2)

# 状態遷移行列 (等速直線運動モデル)
# dt は後で計算
kf.F = np.array([[1, 0, 1, 0],
                 [0, 1, 0, 1],
                 [0, 0, 1, 0],
                 [0, 0, 0, 1]])

# 観測行列 (位置のみを観測)
kf.H = np.array([[1, 0, 0, 0],
                 [0, 1, 0, 0]])

# プロセスノイズ共分散行列
kf.Q = np.eye(4) * 0.4

# 観測ノイズ共分散行列
kf.R = np.eye(2) * 0.8

# 初期状態
kf.x = np.array([[0], [0], [0], [0]])
kf.P = np.eye(4) * 100

# スケーリング係数
scaling_factor = 2.5

def move_mouse(x, y):
    """win32api を使ってマウスを移動する関数。"""
    if DEBUG:
        print(f"Moving mouse to: ({x}, {y})")
    try:
        win32api.SetCursorPos((x, y))
    except Exception as e:
        if DEBUG:
            print(f"Error in SetCursorPos: {e}")
            print(f"  scaled_x: {scaled_x}, scaled_y: {scaled_y}")
            print(f"  filtered_x: {filtered_x}, filtered_y: {filtered_y}")
            print(f"  screen_width: {screen_width}, screen_height: {screen_height}")

def main():
    global screen_width, screen_height, dt, filtered_x, filtered_y, scaled_x, scaled_y
    cap = cv2.VideoCapture(0)
    screen_width, screen_height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

    # FPS を取得して dt を計算
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps > 0:
        dt = 1.0 / fps
    else:
        dt = 1.0 / 30.0  # デフォルト値
    if DEBUG:
        print(f"FPS: {fps}, dt: {dt}")

    # 状態遷移行列を更新
    kf.F[0, 2] = dt
    kf.F[1, 3] = dt

    prev_time = time.time()
    frame_count = 0

    # デバッグ用の時間計測用変数
    times = {
        "frame_read": [],
        "image_processing": [],
        "hand_detection": [],
        "landmark_processing": [],
        "mouse_control": [],
        "drawing": [],
        "total": [],
    }

    while True:
        start_total_time = time.time()

        start_time = time.time()
        success, img = cap.read()
        if not success:
            continue
        times["frame_read"].append(time.time() - start_time)

        start_time = time.time()
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        times["image_processing"].append(time.time() - start_time)

        start_time = time.time()
        results = hands.process(imgRGB)
        times["hand_detection"].append(time.time() - start_time)

        start_time = time.time()
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # ランドマークの描画
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                width, height = img.shape[1], img.shape[0]
                index_finger_tip_pos = np.array([index_finger_tip.x * width, index_finger_tip.y * height]).astype(int)

                # カルマンフィルタの更新
                kf.predict()
                kf.update(index_finger_tip_pos.reshape(-1, 1))

                # フィルタリングされた位置を取得
                filtered_x = int(kf.x[0, 0])
                filtered_y = int(kf.x[1, 0])

                # スケーリング
                scaled_x = int(filtered_x * scaling_factor)
                scaled_y = int(filtered_y * scaling_factor)

                # フィルタリングされた位置に基づいてマウスを移動
                start_mouse_time = time.time()
                move_mouse(scaled_x, scaled_y)
                times["mouse_control"].append(time.time() - start_mouse_time)

                # デバッグ用にフィルタリングされた位置を描画
                if DEBUG:
                    cv2.circle(img, (filtered_x, filtered_y), 10, (0, 0, 255), -1)

            times["landmark_processing"].append(time.time() - start_time)
        else:
            # 手が検出されていない場合は、計測時間を0にする
            times["landmark_processing"].append(0)
            times["mouse_control"].append(0)

        # 描画処理
        start_time = time.time()
        current_time = time.time()
        fps = 1 / (current_time - prev_time) if current_time - prev_time > 0 else 0
        prev_time = current_time
        cv2.putText(img, f"FPS: {fps:.2f}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        times["drawing"].append(time.time() - start_time)

        # 画面表示
        cv2.imshow("Hand Tracking", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        times["total"].append(time.time() - start_total_time)
        frame_count += 1

        # 30フレームごとに平均処理時間を表示
        if frame_count % 30 == 0 and DEBUG:
            print("-" * 30)
            for key, value in times.items():
                # 計測データがある場合のみ平均を計算
                if value:
                    avg_time = np.mean(value)
                    print(f"{key}: {avg_time * 1000:.2f} ms")
                else:
                    print(f"{key}: N/A")
            print(f"FPS: {fps:.2f}")
            print("-" * 30)
            # 時間計測用リストをクリア
            for key in times:
                times[key].clear()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
