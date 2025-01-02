# Hand Tracking Mouse Controller with Kalman Filter

## Overview

#### This project implements a system that controls the mouse cursor using real-time hand tracking with MediaPipe Hands. Kalman filter and win32api are used for high accuracy, low latency tracking and ease of operation.

## Technical and Scientific Background

### MediaPipe Hands

[MediaPipe Hands](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker) is a framework developed by Google that provides high-fidelity hand and finger tracking by employing machine learning (ML) to infer 21 3D landmarks of a hand from just a single frame. This system uses MediaPipe Hands to detect the hand position and its 21 landmarks (e.g., finger joints) in real-time from camera input.

### Kalman Filter

The Kalman filter is an algorithm that uses a series of measurements observed over time, containing statistical noise and other inaccuracies, and produces estimates of unknown variables that tend to be more accurate than those based on a single measurement alone, by estimating a joint probability distribution over the variables for each timeframe. The filter is named after Rudolf E. Kálmán, one of the primary developers of its theory.

The Kalman filter has two distinct phases: **Predict** and **Update**.

*   **Predict phase:** The Kalman filter produces estimates of the current state variables, along with their uncertainties, based on the system model.
*   **Update phase:** The next measurement is used to refine these predictions by a weighted average, with more weight being given to estimates with higher certainty.

In this system, the hand position is considered the state, and the landmark positions obtained from MediaPipe Hands are the observed values. A constant velocity model is assumed, and the state is estimated using the following equations:

**State Transition Matrix (F):**
content_copy
download
Use code with caution.
Markdown

```math
Q = \begin{bmatrix} q1 & 0 & 0 & 0 \\ 0 & q2 & 0 & 0 \\ 0 & 0 & q3 & 0 \\ 0 & 0 & 0 & q4 \end{bmatrix}
```
where `dt` is the time interval between frames.

**Observation Matrix (H):**
content_copy
download
Use code with caution.

H = | 1 0 0 0 |
| 0 1 0 0 |

**Process Noise Covariance Matrix (Q):**
content_copy
download
Use code with caution.

Q = | q1 0 0 0 |
| 0 q2 0 0 |
| 0 0 q3 0 |
| 0 0 0 q4 |

where `q1`, `q2`, `q3`, and `q4` are parameters representing the magnitude of process noise.

**Measurement Noise Covariance Matrix (R):**
content_copy
download
Use code with caution.

R = | r1 0 |
| 0 r2 |

where `r1` and `r2` are parameters representing the magnitude of measurement noise.

By applying the Kalman filter, the noisy hand position data obtained from MediaPipe Hands is smoothed, resulting in smoother and more accurate mouse cursor movement.

### Mouse Control

The `win32api` library is used for mouse cursor control. The `win32api.SetCursorPos()` function moves the mouse cursor to the hand position estimated by the Kalman filter.

### Sensitivity Adjustment

The sensitivity of the mouse cursor (the amount of mouse cursor movement relative to hand movement) can be adjusted using the scaling factor `scaling_factor`. Increasing this factor increases the sensitivity. Fine-tuning of the sensitivity can also be achieved by adjusting the Kalman filter parameters `Q` and `R`.

## Operating Environment

*   Windows 10/11
*   Python 3.7+

## Required Libraries

*   mediapipe
*   opencv-python
*   numpy
*   filterpy
*   pywin32

## Installation

```bash
pip install mediapipe opencv-python numpy filterpy pywin32
```
Place your hand in front of the camera, and the mouse cursor will move according to your hand movements.

### Configuration

DEBUG (Default: False): Set to True to output debug information.

scaling_factor (Default: 2.5): Adjusts the sensitivity of the mouse cursor.

kf.Q (Default: np.eye(4) * 0.4): Process noise covariance matrix for the Kalman filter.

kf.R (Default: np.eye(2) * 0.8): Measurement noise covariance matrix for the Kalman filter.

These parameters can be configured at the beginning of main.py.

### Troubleshooting

Program does not start: Ensure that all required libraries are installed.

Hand is not detected: Verify that the camera is connected correctly and that the operating environment meets the requirements of MediaPipe Hands.

Mouse cursor does not move: Check if win32api is installed correctly. You may need to run the script with administrator privileges.

Performance is slow: Lowering the values of min_detection_confidence and min_tracking_confidence may improve performance but could reduce accuracy.

### Contribution

Contributions to this project are welcome. Whether it's reporting bugs, suggesting features, or submitting pull requests, your contributions are appreciated.

### License

This project is released under the MIT License. See the LICENSE file for details.

Acknowledgements

This project utilizes the MediaPipe Hands and filterpy libraries. We thank the developers of these excellent libraries.




# Hand Tracking Mouse Controller with Kalman Filter

## Overview

This project implements a system that controls the mouse cursor using real-time hand tracking with MediaPipe Hands. Kalman filter and win32api are used for high accuracy, low latency tracking and ease of operation.

## Technical and Scientific Background

### MediaPipe Hands

[MediaPipe Hands](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker) is a framework developed by Google that provides high-fidelity hand and finger tracking by employing machine learning (ML) to infer 21 3D landmarks of a hand from just a single frame. This system uses MediaPipe Hands to detect the hand position and its 21 landmarks (e.g., finger joints) in real-time from camera input.

### Kalman Filter

The Kalman filter is an algorithm that uses a series of measurements observed over time, containing statistical noise and other inaccuracies, and produces estimates of unknown variables that tend to be more accurate than those based on a single measurement alone, by estimating a joint probability distribution over the variables for each timeframe. The filter is named after Rudolf E. Kálmán, one of the primary developers of its theory.

The Kalman filter has two distinct phases: **Predict** and **Update**.

*   **Predict phase:** The Kalman filter produces estimates of the current state variables, along with their uncertainties, based on the system model.
*   **Update phase:** The next measurement is used to refine these predictions by a weighted average, with more weight being given to estimates with higher certainty.

In this system, the hand position is considered the state, and the landmark positions obtained from MediaPipe Hands are the observed values. A constant velocity model is assumed, and the state is estimated using the following equations:

**State Transition Matrix (F):**

```math
F = \begin{bmatrix} 1 & 0 & dt & 0 \\ 0 & 1 & 0 & dt \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}
```

where `dt` is the time interval between frames.

**Observation Matrix (H):**

```math
H = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \end{bmatrix}
```

**Process Noise Covariance Matrix (Q):**

```math
Q = \begin{bmatrix} q1 & 0 & 0 & 0 \\ 0 & q2 & 0 & 0 \\ 0 & 0 & q3 & 0 \\ 0 & 0 & 0 & q4 \end{bmatrix}
```

where `q1`, `q2`, `q3`, and `q4` are parameters representing the magnitude of process noise.

**Measurement Noise Covariance Matrix (R):**

```math
R = \begin{bmatrix} r1 & 0 \\ 0 & r2 \end{bmatrix}
```

where `r1` and `r2` are parameters representing the magnitude of measurement noise.

By applying the Kalman filter, the noisy hand position data obtained from MediaPipe Hands is smoothed, resulting in smoother and more accurate mouse cursor movement.

### Mouse Control

The `win32api` library is used for mouse cursor control. The `win32api.SetCursorPos()` function moves the mouse cursor to the hand position estimated by the Kalman filter.

### Sensitivity Adjustment

The sensitivity of the mouse cursor (the amount of mouse cursor movement relative to hand movement) can be adjusted using the scaling factor `scaling_factor`. Increasing this factor increases the sensitivity. Fine-tuning of the sensitivity can also be achieved by adjusting the Kalman filter parameters `Q` and `R`.

## Operating Environment

*   Windows 10/11
*   Python 3.7+

## Required Libraries

*   mediapipe
*   opencv-python
*   numpy
*   filterpy
*   pywin32

## Installation

```bash
pip install mediapipe opencv-python numpy filterpy pywin32
```

## Usage
1. Run 
    ```bash
    python hand_tracking_mouse_controller.py
    ```
2. Place your hand in front of the camera, and the mouse cursor will move according to your hand movements.

## Configuration

*   **`DEBUG` (Default: `False`):** Set to `True` to output debug information.
*   **`scaling_factor` (Default: `2.5`):** Adjusts the sensitivity of the mouse cursor.
*   **`kf.Q` (Default: `np.eye(4) * 0.4`):** Process noise covariance matrix for the Kalman filter.
*   **`kf.R` (Default: `np.eye(2) * 0.8`):** Measurement noise covariance matrix for the Kalman filter.

These parameters can be configured at the beginning of `main.py`.

## Troubleshooting

*   **Program does not start:** Ensure that all required libraries are installed.
*   **Hand is not detected:** Verify that the camera is connected correctly and that the operating environment meets the requirements of MediaPipe Hands.
*   **Mouse cursor does not move:** Check if `win32api` is installed correctly. You may need to run the script with administrator privileges.
*   **Performance is slow:** Lowering the values of `min_detection_confidence` and `min_tracking_confidence` may improve performance but could reduce accuracy.

## Contribution

Contributions to this project are welcome. Whether it's reporting bugs, suggesting features, or submitting pull requests, your contributions are appreciated.

## License

This project is released under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

This project utilizes the MediaPipe Hands and filterpy libraries. We thank the developers of these excellent libraries.













# Hand Tracking Mouse Controller with Kalman Filter

## 概要

このプロジェクトは、MediaPipe Hands を使用してリアルタイムに手の動きを検出し、その情報を用いてマウスカーソルを制御するシステムです。カルマンフィルタと win32api を使用することで、高精度、低遅延なトラッキングと容易な操作性を実現しています。

## 技術的・学術的背景

### MediaPipe Hands

[MediaPipe Hands](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker) は、Google が開発した、機械学習を用いて高精度な手の検出とランドマーク推定を行うフレームワークです。このシステムでは、MediaPipe Hands を用いて、カメラから入力された画像から手の位置と 21 個のランドマーク (指の関節など) をリアルタイムに検出します。

### カルマンフィルタ

カルマンフィルタは、誤差のある観測値を用いて、動的システムの状態を推定するためのアルゴリズムです。時間とともに変化するシステムの状態を、**予測**と**更新**の 2 つのステップを繰り返すことで推定します。

*   **予測ステップ:** システムのモデルに基づいて、現在の状態から次の状態を予測します。
*   **更新ステップ:** 観測値を用いて、予測された状態を修正します。

このシステムでは、手の位置を状態とし、MediaPipe Hands から得られるランドマークの位置を観測値として、カルマンフィルタを適用しています。等速直線運動モデルを仮定し、以下の式で状態を推定します。

**状態遷移行列 (F):**

```math
F = \begin{bmatrix} 1 & 0 & dt & 0 \\ 0 & 1 & 0 & dt \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}
```

ここで、`dt` はフレーム間の時間です。

**観測行列 (H):**

```math
H = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \end{bmatrix}
```

**プロセスノイズ共分散行列 (Q):**

```math
Q = \begin{bmatrix} q1 & 0 & 0 & 0 \\ 0 & q2 & 0 & 0 \\ 0 & 0 & q3 & 0 \\ 0 & 0 & 0 & q4 \end{bmatrix}
```

ここで、`q1`, `q2`, `q3`, `q4` はプロセスノイズの大きさを表すパラメータです。

**観測ノイズ共分散行列 (R):**

```math
R = \begin{bmatrix} r1 & 0 \\ 0 & r2 \end{bmatrix}
```

ここで、`r1`, `r2` は観測ノイズの大きさを表すパラメータです。

カルマンフィルタを適用することで、MediaPipe Hands から得られるノイズの多い手の位置情報を平滑化し、より滑らかで正確なマウスカーソルの動きを実現しています。

### マウス制御

マウスカーソルの制御には、`win32api` ライブラリを使用しています。`win32api.SetCursorPos()` 関数を用いて、カルマンフィルタによって推定された手の位置にマウスカーソルを移動させています。

### 感度調整

マウスカーソルの感度 (手の動きに対するマウスカーソルの移動量) は、スケーリング係数 `scaling_factor` によって調整できます。この係数を大きくすると、感度が向上します。また、カルマンフィルタのパラメータ `Q` と `R` を調整することでも、感度を微調整できます。

## 動作環境

*   Windows 10/11
*   Python 3.7 以上

## 必要なライブラリ

*   mediapipe
*   opencv-python
*   numpy
*   filterpy
*   pywin32

## インストール方法

```bash
pip install mediapipe opencv-python numpy filterpy pywin32
```

## 使用方法

1. 以下を実行します
    ```bash
    python main.py
    ```
2. カメラに手をかざすと、手の動きに合わせてマウスカーソルが動きます。

## 設定

*   **`DEBUG` (デフォルト: `False`):** `True` に設定すると、デバッグ情報が出力されます。
*   **`scaling_factor` (デフォルト: `2.5`):** マウスカーソルの感度を調整します。
*   **`kf.Q` (デフォルト: `np.eye(4) * 0.4`):** カルマンフィルタのプロセスノイズ共分散行列。
*   **`kf.R` (デフォルト: `np.eye(2) * 0.8`):** カルマンフィルタの観測ノイズ共分散行列。

これらのパラメータは、`main.py` の先頭部分で設定できます。

## トラブルシューティング

*   **プログラムが起動しない:** 必要なライブラリがすべてインストールされていることを確認してください。
*   **手が検出されない:** カメラが正しく接続されていること、および MediaPipe Hands の動作環境を満たしていることを確認してください。
*   **マウスカーソルが動かない:** `win32api` が正しくインストールされていることを確認してください。また、管理者権限で実行する必要がある場合があります。
*   **動作が重い:** `min_detection_confidence` や `min_tracking_confidence` の値を下げると、処理が軽くなる可能性がありますが、精度が低下する可能性があります。

## 貢献

このプロジェクトへの貢献は大歓迎です。バグの報告、機能の提案、プルリクエストなど、どのような形でも貢献していただければ幸いです。

## ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。詳細は `LICENSE` ファイルをご覧ください。

## 謝辞

このプロジェクトは、MediaPipe Hands と filterpy ライブラリを使用しています。ライブラリの開発者に感謝します。

