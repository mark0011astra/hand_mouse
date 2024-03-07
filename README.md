# hand_mouse
## Hand Tracking-Based Mouse Controller

This project is an advanced implementation that allows controlling the mouse cursor using hand gestures captured through a webcam. It utilizes computer vision and hand tracking technologies to translate hand movements and gestures into cursor movements and mouse clicks.

## Features

- **Hand Tracking**: Leverages MediaPipe for real-time hand tracking.
- **Cursor Movement**: Maps the index finger's movement to the mouse cursor.
- **Click Detection**: Detects a click action when the thumb and index finger tips are close together.
- **Moving Average Filter**: Applies a moving average filter to smooth the cursor's movement.

## Requirements

- Python 3.6 or later
- OpenCV (`cv2`): For capturing video input from the webcam and displaying the output.
- MediaPipe (`mediapipe`): For hand tracking.
- NumPy (`numpy`): For numerical operations.
- PyAutoGUI (`pyautogui`): For controlling the mouse cursor.

## Installation

To install the required libraries, run:

```bash
pip install opencv-python mediapipe numpy pyautogui
```

## Usage

To start the hand tracking mouse controller, run:

```bash
python hand_tracking_mouse_controller.py
```

Ensure your webcam is accessible and not being used by another application.

## How It Works

1. **Initialization**: Sets up hand tracking with MediaPipe and retrieves screen resolution using PyAutoGUI.
2. **Video Capture**: Continuously captures video frames from the webcam.
3. **Hand Detection**: Each frame is processed to detect the hand and identify landmarks such as the thumb tip and index finger tip.
4. **Cursor Movement**: Calculates the position of the index finger tip and applies a moving average filter to smooth the movement. The cursor's screen position is scaled based on the detected position.
5. **Click Detection**: Determines if a click action should be performed based on the distance between the thumb tip and index finger tip.
6. **Action Execution**: Moves the mouse cursor and performs click actions accordingly.

## Customization

- **Cursor Sensitivity**: Adjust the mapping between hand movement and cursor movement by modifying the scaling factors.
- **Click Sensitivity**: Change the distance threshold for click detection to suit your preference.

## Quitting the Application

Press `q` while the output window is focused to safely close the application.

## Index_finger_detection_only.py
Index_finger_detection_only.py is an implementation that does not actually operate the mouse cursor, but only displays the index finger position and click detection on the Window.

## License

This project is open source and available under the MIT License.


# 手の動きによるマウスカーソル操作

このプロジェクトは、ウェブカメラを通じてキャプチャされた手のジェスチャーを使用してマウスカーソルを制御するための実装です。コンピュータビジョンと手のトラッキング技術を活用して、手の動きとジェスチャーをカーソルの動きとマウスクリックに変換します。

## 特徴

- **手のトラッキング**: MediaPipeを利用したリアルタイムの手のトラッキング。
- **カーソルの動き**: 人差し指の動きをマウスカーソルにマッピング。
- **クリック検出**: 親指と人差し指の先が近づいたときにクリックアクションを検出。
- **移動平均フィルタ**: カーソルの動きを滑らかにするための移動平均フィルタを適用。

## 必要条件

- Python 3.6以降
- OpenCV (`cv2`): ウェブカメラからのビデオ入力をキャプチャし、出力を表示するため。
- MediaPipe (`mediapipe`): 手のトラッキングのため。
- NumPy (`numpy`): 数値演算のため。
- PyAutoGUI (`pyautogui`): マウスカーソルを制御するため。

## インストール

必要なライブラリをインストールするには、以下を実行してください:

```bash
pip install opencv-python mediapipe numpy pyautogui
```

## 使用方法

手のトラッキングマウスコントローラーを起動するには、以下を実行してください:

```bash
python hand_tracking_mouse_controller.py
```

ウェブカメラがアクセス可能であり、他のアプリケーションに使用されていないことを確認してください。

## 動作原理

1. **初期化**: MediaPipeで手のトラッキングを設定し、PyAutoGUIを使用して画面解像度を取得。
2. **ビデオキャプチャ**: ウェブカメラからビデオフレームを連続してキャプチャ。
3. **手の検出**: 各フレームを処理して手を検出し、親指の先や人差し指の先などのランドマークを識別。
4. **カーソルの動き**: 人差し指の先の位置を計算し、移動を滑らかにするために移動平均フィルタを適用。検出された位置に基づいてカーソルの画面位置をスケーリング。
5. **クリック検出**: 親指の先と人差し指の先の距離に基づいて、クリックアクションを実行するかどうかを決定。
6. **アクション実行**: マウスカーソルを移動させ、必要に応じてクリックアクションを実行。

## カスタマイズ

- **カーソルの感度**: 手の動きとカーソルの動きのマッピングを調整するために、スケーリングファクターを変更します。
- **クリックの感度**: クリック検出のための距離閾値を、好みに合わせて変更します。

## アプリケーションの終了方法

出力ウィンドウがフォーカスされている状態で `q` を押すと、アプリケーションを安全に閉じることができます。

## Index_finger_detection_only.py
Index_finger_detection_only.pyは、実際にマウスカーソルを操作するのではなく、人差し指の位置とクリックの検出をWindow上に表示するだけの実装です。

## ライセンス

このプロジェクトはオープンソースであり、MITライセンスの下で利用可能です。



