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
        self.plot_data_item = self.plot_widget.plot(pen='y')

        # グラフの初期値を設定
        self.plot_data_item.setData(np.zeros(8))

        # タイマーを設定して定期的にデータを受信する
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50)

    def update_plot(self):
        # データを取得してプロット
        sample, timestamp = self.inlet.pull_sample()
        self.plot_data_item.setData(np.hstack((self.plot_data_item.getData()[0][1:], sample)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
