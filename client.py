import sys
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication
import pyqtgraph as pg
from pylsl import resolve_stream, StreamInlet
import time


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # データストリームを検索して、StreamInletオブジェクトを作成する
        stream_name = 'XHRO-81e5-EEG'  # Streamの名前
        stream_channels = 8  # Streamのチャンネル数
        self.inlet = None
        while self.inlet is None:
            print("Looking for stream...")
            streams = resolve_stream('name', 'XHRO-81e5-EEG')
            if len(streams) > 0:
                self.inlet = StreamInlet(streams[0], max_buflen=360)
        print(f"Connected to stream '{stream_name}' with {stream_channels} channels.")

        # グラフを作成
        self.plot_widget = pg.PlotWidget()
        self.setCentralWidget(self.plot_widget)
        self.plot_data_item = self.plot_widget.plot()
        self.plot_data_item.setPen(pg.mkPen(color=(255, 0, 0), width=2))
        self.plot_widget.setYRange(-100, 100)

        # ウィンドウサイズを設定
        self.setGeometry(100, 100, 800, 600)

        # タイマーを設定して定期的にデータを受信する
        self.timer = pg.QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50)

    def closeEvent(self, event):
        # タイマーを停止する
        self.timer.stop()
        event.accept()

    def update_plot(self):
        # データを取得してプロット
        sample, timestamp = self.inlet.pull_sample()
        # データをプロットする
        self.plot_data_item.setData(sample)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
