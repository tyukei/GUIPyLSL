import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
import numpy as np
from pylsl import resolve_stream, StreamInlet


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # ストリームを検索してStreamInletオブジェクトを作成
        streams = resolve_stream('name', 'XHRO-81e5-OPT')
        self.inlet = StreamInlet(streams[0])

        # グラフを作成
        self.plot_widget = pg.PlotWidget()
        self.setCentralWidget(self.plot_widget)

        # ウィンドウサイズを設定
        self.setGeometry(100, 100, 800, 600)

        # グラフの初期値を設定
        self.plot_data_items = []
        for i in range(8):
            pen = pg.mkPen(color=(255 * i / 8, 0, 255 * (8 - i) / 8), width=2)
            plot_data_item = self.plot_widget.plot(pen=pen)
            plot_data_item.setData(np.zeros(1000) + i)
            self.plot_data_items.append(plot_data_item)

        # グラフの横軸範囲を設定
        self.plot_widget.setXRange(0, 1000)

        # タイマーを設定して定期的にデータを受信する
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50)

        # ボタンを作成してウィンドウに追加
        self.pause_button = QPushButton('Pause', self)
        self.pause_button.clicked.connect(self.pause_plot)
        self.play_button = QPushButton('Play', self)
        self.play_button.clicked.connect(self.play_plot)
        self.toolbar = self.addToolBar('')
        self.toolbar.addWidget(self.pause_button)
        self.toolbar.addWidget(self.play_button)

        # プロットの一時停止フラグ
        self.plot_paused = False

    def pause_plot(self):
        self.plot_paused = True

    def play_plot(self):
        self.plot_paused = False

    def closeEvent(self, event):
        # タイマーを停止する
        self.timer.stop()
        event.accept()

    def update_plot(self):
        # データを取得してプロット
        if self.plot_paused:
            return
        sample, timestamp = self.inlet.pull_sample()
        data = np.array([plot_data_item.getData()[1] for plot_data_item in self.plot_data_items])
        data = np.array(data)
        sample = np.array(sample)
        data = np.hstack((data[:, 1:], sample.reshape(-1, 1)))

        # dataの長さが1000を超えている場合は、先頭から1000個だけを使用する
        if len(data[0]) > 1000:
            data = data[:, -1000:]

        # プロットアイテムごとに色を設定する
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                  (0, 255, 255), (255, 0, 255), (128, 0, 128), (255, 128, 0)]
        for i, plot_data_item in enumerate(self.plot_data_items):
            plot_data_item.setData(data[i, :])
            plot_data_item.setPen(pg.mkPen(color=colors[i], width=2))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
