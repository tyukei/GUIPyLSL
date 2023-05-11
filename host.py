import sys
import numpy as np
from pylsl import StreamInlet, resolve_stream
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # ストリームを検索してStreamInletオブジェクトを作成
        streams = resolve_stream('name', 'MyStream')
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
            plot_data_item.setData(np.zeros(10000) + i)
            self.plot_data_items.append(plot_data_item)

        # グラフの横軸範囲を設定
        self.plot_widget.setXRange(0, 10000)

        # タイマーを設定して定期的にデータを受信する
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50)

    def update_plot(self):
        # データを取得してプロット
        sample, timestamp = self.inlet.pull_sample()
        data = np.array([plot_data_item.getData()[1] for plot_data_item in self.plot_data_items])
        data = np.array(data)
        sample = np.array(sample)
        data = np.hstack((data[:, 1:], sample.reshape(-1, 1)))

        # dataの長さが1000を超えている場合は、先頭から最新の1000個だけを使用する
        if len(data[0]) > 10000:
            data = data[:, -10000:]

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
