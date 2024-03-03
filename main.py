import cv2
import mediapipe as mp
import numpy as np

# マウスカーソルを模倣するための設定
cursor_radius = 10
cursor_color = (255, 0, 0)  # 赤色
click_color = (0, 255, 0)  # クリック時は緑色

# ハンドトラッキングの初期化
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

def draw_cursor(img, position, clicked=False):
    """マウスカーソル（円）を描画する関数。クリック状態に応じて色を変える。"""
    color = click_color if clicked else cursor_color
    cv2.circle(img, position, cursor_radius, color, -1)

def check_thumb_index_finger_click(landmarks_coordinates):
    """親指と人差し指がタップされたかどうかを検出する関数。"""
    thumb_tip = landmarks_coordinates[4][:2]
    index_finger_tip = landmarks_coordinates[8][:2]
    distance = np.linalg.norm(np.array(thumb_tip) - np.array(index_finger_tip))
    return distance < 0.1  # 適切な閾値に調整する必要があるかもしれません

def main():
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        if not success:
            break

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        clicked = False

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks_coordinates = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
                # カーソルの位置を人差し指の先端に設定
                index_finger_tip = landmarks_coordinates[8]
                cursor_position = (int(index_finger_tip[0] * img.shape[1]), int(index_finger_tip[1] * img.shape[0]))
                
                # クリック状態の検出
                clicked = check_thumb_index_finger_click(landmarks_coordinates)

                draw_cursor(img, cursor_position, clicked)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()
