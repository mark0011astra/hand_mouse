import cv2
import mediapipe as mp
import numpy as np
import pyautogui

# マウスカーソルを模倣するための設定（ここでは使用しない）
cursor_radius = 10
cursor_color = (0, 255, 0)  # 通常時は緑
click_color = (0, 0, 255)  # クリック時は赤色

# ハンドトラッキングの初期化
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 移動平均フィルタ用のリスト
cursor_positions = []

def apply_moving_average(new_position):
    """移動平均フィルタを適用する関数。"""
    cursor_positions.append(new_position)
    if len(cursor_positions) > 3:  # 最新の3つの位置を使用
        cursor_positions.pop(0)
    return np.mean(cursor_positions, axis=0).astype(int)

def main():
    cap = cv2.VideoCapture(0)
    screen_width, screen_height = pyautogui.size()  # スクリーンの解像度を取得

    while True:
        success, img = cap.read()
        if not success:
            continue

        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                thumb_tip_pos = np.array([thumb_tip.x, thumb_tip.y])
                index_finger_tip_pos = np.array([index_finger_tip.x, index_finger_tip.y])

                width, height = img.shape[1], img.shape[0]
                thumb_tip_pos_scaled = np.multiply(thumb_tip_pos, [width, height]).astype(int)
                index_finger_tip_pos_scaled = np.multiply(index_finger_tip_pos, [width, height]).astype(int)

                smoothed_position = apply_moving_average(index_finger_tip_pos_scaled)

                # スクリーン解像度に合わせて座標をスケーリング
                scaled_x = np.interp(smoothed_position[0], [0, width], [0, screen_width])
                scaled_y = np.interp(smoothed_position[1], [0, height], [0, screen_height])

                distance = np.linalg.norm(thumb_tip_pos_scaled - index_finger_tip_pos_scaled)
                clicked = distance < 20  # 距離が20ピクセル未満であればクリックと判定

                pyautogui.moveTo(scaled_x, scaled_y)  # マウスカーソルを移動
                if clicked:
                    pyautogui.click()  # マウスクリック操作を実行

        cv2.imshow("Hand Tracking", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
