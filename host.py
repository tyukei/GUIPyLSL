import sys
import numpy as np
from pylsl import StreamInfo, StreamOutlet
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # ストリーム情報を作成しストリームアウトレットを作成
        stream_info = StreamInfo('MyStream', 'Data', 2, 100, 'float32', 'myuid2424')
        self.outlet = StreamOutlet(stream_info)

        # グラフを作成
        self.plot_widget = pg.PlotWidget()
        self.setCentralWidget(self.plot_widget)
        self.plot_data_item = self.plot_widget.plot(pen='y')

        # タイマーを設定して定期的にデータを送信する
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.send_data)
        self.timer.start(1000)

    def send_data(self):
        # 時間と sin 波の値を含んだデータを生成し送信
        t = np.linspace(0, 1, 100)
        data = np.vstack([t, np.sin(2 * np.pi * 10 * t)]).T
        self.outlet.push_chunk(data.tolist())

        # データをプロット
        self.plot_data_item.setData(data[:, 0], data[:, 1])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

