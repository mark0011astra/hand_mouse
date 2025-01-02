# Hand Tracking Mouse Controller with Kalman Filter

## 概要

このプロジェクトは、MediaPipe Hands を使用してリアルタイムに手の動きを検出し、その情報を用いてマウスカーソルを制御するシステムです。手の位置推定にはカルマンフィルタを適用し、ノイズの多い観測データから滑らかで正確なマウス操作を実現します。

## 技術的・学術的背景

### MediaPipe Hands

[MediaPipe Hands](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker) は、Google が開発した、機械学習を用いて高精度な手の検出とランドマーク推定を行うフレームワークです。このシステムでは、MediaPipe Hands を用いて、カメラから入力された画像から手の位置と 21 個のランドマーク (指の関節など) をリアルタイムに検出します。

### カルマンフィルタ

カルマンフィルタは、誤差のある観測値を用いて、動的システムの状態を推定するためのアルゴリズムです。時間とともに変化するシステムの状態を、**予測**と**更新**の 2 つのステップを繰り返すことで推定します。

*   **予測ステップ:** システムのモデルに基づいて、現在の状態から次の状態を予測します。
*   **更新ステップ:** 観測値を用いて、予測された状態を修正します。

このシステムでは、手の位置を状態とし、MediaPipe Hands から得られるランドマークの位置を観測値として、カルマンフィルタを適用しています。等速直線運動モデルを仮定し、以下の式で状態を推定します。

**状態遷移行列 (F):**
content_copy
download
Use code with caution.
Markdown

F = | 1 0 dt 0 |
| 0 1 0 dt |
| 0 0 1 0 |
| 0 0 0 1 |

ここで、`dt` はフレーム間の時間です。

**観測行列 (H):**
content_copy
download
Use code with caution.

H = | 1 0 0 0 |
| 0 1 0 0 |

**プロセスノイズ共分散行列 (Q):**
content_copy
download
Use code with caution.

Q = | q1 0 0 0 |
| 0 q2 0 0 |
| 0 0 q3 0 |
| 0 0 0 q4 |

ここで、`q1`, `q2`, `q3`, `q4` はプロセスノイズの大きさを表すパラメータです。

**観測ノイズ共分散行列 (R):**
content_copy
download
Use code with caution.

R = | r1 0 |
| 0 r2 |

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
main.py を実行します。


カメラに手をかざすと、手の動きに合わせてマウスカーソルが動きます。

### 設定

DEBUG (デフォルト: False): True に設定すると、デバッグ情報が出力されます。

scaling_factor (デフォルト: 2.5): マウスカーソルの感度を調整します。

kf.Q (デフォルト: np.eye(4) * 0.4): カルマンフィルタのプロセスノイズ共分散行列。

kf.R (デフォルト: np.eye(2) * 0.8): カルマンフィルタの観測ノイズ共分散行列。

これらのパラメータは、main.py の先頭部分で設定できます。

#### トラブルシューティング

プログラムが起動しない: 必要なライブラリがすべてインストールされていることを確認してください。

手が検出されない: カメラが正しく接続されていること、および MediaPipe Hands の動作環境を満たしていることを確認してください。

マウスカーソルが動かない: win32api が正しくインストールされていることを確認してください。また、管理者権限で実行する必要がある場合があります。

動作が重い: min_detection_confidence や min_tracking_confidence の値を下げると、処理が軽くなる可能性がありますが、精度が低下する可能性があります。

### 貢献

このプロジェクトへの貢献は大歓迎です。バグの報告、機能の提案、プルリクエストなど、どのような形でも貢献していただければ幸いです。

ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。詳細は LICENSE ファイルをご覧ください。

### 謝辞

このプロジェクトは、MediaPipe Hands と filterpy ライブラリを使用しています。これらの素晴らしいライブラリの開発者に感謝します。
