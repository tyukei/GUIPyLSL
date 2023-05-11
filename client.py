import time
import numpy as np
from pylsl import StreamInfo, StreamOutlet, pylsl

# ストリーム情報を作成する
info = StreamInfo('MyStream', 'EEG', 8, 250, 'float32', 'myuid')
outlet = StreamOutlet(info)

# サンプルレートを定義
fs = 250

# ｎ分間のサンプル数を計算
n_samples = fs * 60 * 5

# サイン波の周波数と振幅を定義
freq = 10  # 10 Hz
amp = 1

# サイン波の波形を生成
t = np.arange(n_samples) / fs
waveform = amp * np.sin(2 * np.pi * freq * t)

# サンプルをストリームに送信
for i in range(n_samples):
    sample = [waveform[i % len(waveform)]] * 8
    outlet.push_sample(sample)
    time.sleep(1/fs)

print(pylsl.resolve_stream())
