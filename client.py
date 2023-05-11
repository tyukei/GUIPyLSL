from pylsl import StreamInfo, StreamOutlet
import math
import time


# ストリーム情報を定義
stream_name = "MyStream"
stream_type = "EEG"
n_channels = 8
srate = 250
dtype = "float32"
stream_info = StreamInfo(stream_name, stream_type, n_channels, srate, dtype, "myuid")
outlet = StreamOutlet(stream_info)

# 1分間にわたってsin波を生成してストリームに送信
start_time = time.time()
while time.time() - start_time < 60:
    # sin波を生成
    t = time.time() - start_time
    data = [[math.sin(i * 2 * math.pi * f * t) for i in range(n_channels)] for f in range(1, 9)]

    # データをストリームに送信
    outlet.push_sample(data)

    # 1秒間隔で出力
    time.sleep(1)


print(pylsl.resolve_stream())