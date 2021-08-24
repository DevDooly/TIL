import cv2
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage, QPixmap, QIcon


class VideoLabel(QLabel):

    def __init__(self, url):
        super(VideoLabel, self).__init__()
        self.setAutoFillBackground(True)
        self.setScaledContents(True)
        self.setStyleSheet("background-color: #000000;")

        self.url = url
        self.thread = VideoThread(self.url)

    def set_image(self, image):
        self.setPixmap(QPixmap.fromImage(image))

    def showEvent(self, event):
        self.thread = VideoThread(self.url)
        self.thread.changePixmap.connect(self.set_image)
        self.thread.start()

    def hideEvent(self, event):
        self.thread.stop()

    def restart(self):
        self.thread.stop()
        self.thread = VideoThread(self.url)
        self.thread.changePixmap.connect(self.set_image)
        self.thread.start()


class VideoThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self, url):
        super(VideoThread, self).__init__()
        self.working = True
        self.url = url

    def run(self):
        if not self.url:
            return

        cap = cv2.VideoCapture(self.url)
        while self.working:
            ret, frame = cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_qt_format = QImage(rgb_image.data,
                                              w,
                                              h,
                                              bytes_per_line,
                                              QImage.Format_RGB888)

                self.changePixmap.emit(convert_to_qt_format)

    def stop(self):
        self.working = False
        self.sleep(1)


if __name__ == '__main__':
    sample_url = 'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov'
    app = QApplication(sys.argv)
    main = VideoWidget(sample_url)
    main.resize(640, 480)
    main.show()
    sys.exit(app.exec_())
