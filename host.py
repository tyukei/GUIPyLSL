import time
import numpy as np
from pylsl import StreamInfo, StreamOutlet, pylsl

# ストリーム情報を作成する
info = StreamInfo('MyStream', 'EEG', 8, 250, 'float32', 'myuid')
outlet = StreamOutlet(info)

# サンプルレートを定義
fs = 250

# 1分間のサンプル数を計算
n_samples = fs * 60

# 8つの周波数をランダムに選択
freqs = np.random.choice(range(1, 21), size=8, replace=False)

# 8つの振幅を指定
amplitudes = [1, 2, 3, 4, 5, 6, 7, 8]

# 矩形波の波形を生成
t = np.arange(n_samples) / fs
waveform = np.zeros((n_samples, 8))
for i, (freq, amp) in enumerate(zip(freqs, amplitudes)):
    waveform[:, i] = np.where(np.sin(2 * np.pi * freq * t) > 0, amp, -amp)

# サンプルをストリームに送信
for i in range(n_samples):
    sample = waveform[i % len(waveform)]
    outlet.push_sample(sample)
    time.sleep(1/fs)

print(pylsl.resolve_stream())
