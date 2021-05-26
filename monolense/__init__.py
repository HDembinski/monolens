__version__ = "0.1.1"


def main():
    from PySide6.QtWidgets import QWidget, QApplication
    from PySide6.QtCore import Qt, QTimer
    from PySide6.QtGui import QGuiApplication, QImage, QPainter
    import sys

    class Main(QWidget):
        def __init__(self):
            QWidget.__init__(self)
            self.setWindowFlag(Qt.FramelessWindowHint)
            self.setWindowFlag(Qt.WindowStaysOnTopHint)
            self.updateScreen()

        def refresh(self):
            self.repaint(0, 0, self.width(), self.height())

        def updateScreen(self):
            screen = QGuiApplication.primaryScreen()
            wh = self.windowHandle()
            if wh:
                screen = wh.screen()
            if not screen:
                return
            image = screen.grabWindow(0).toImage()
            image = image.convertToFormat(QImage.Format_Grayscale8)
            self._screen = image

        def paintEvent(self, event):
            x = self.x()
            y = self.y()
            w = self.width()
            h = self.height()
            p = QPainter(self)
            dpr = self.devicePixelRatio()
            p.drawImage(0, 0, self._screen, x * dpr, max(0, y * dpr), w * dpr, h * dpr)
            p.end()
            super(Main, self).paintEvent(event)

        def resizeEvent(self, event):
            self.refresh()
            super(Main, self).resizeEvent(event)

        def moveEvent(self, event):
            self.refresh()
            super(Main, self).moveEvent(event)

        def keyPressEvent(self, event):
            key = event.key()
            if key in (Qt.Key_Escape, Qt.Key_Q):
                self.close()
            elif key == Qt.Key_Space:
                self.hide()
                QTimer.singleShot(0, self.show)
            elif key == Qt.Key_Left:
                x = self.x()
                y = self.y()
                w = max(50, self.width() - 50)
                h = self.height()
                self.move(x + 25, y)
                self.resize(w, h)
            elif key == Qt.Key_Right:
                x = self.x()
                y = self.y()
                w = self.width() + 50
                h = self.height()
                self.move(x - 25, y)
                self.resize(w, h)
            elif key == Qt.Key_Down:
                x = self.x()
                y = self.y()
                w = self.width()
                h = max(50, self.height() - 50)
                self.move(x, y + 25)
                self.resize(w, h)
            elif key == Qt.Key_Up:
                x = self.x()
                y = self.y()
                w = self.width()
                h = self.height() + 50
                self.move(x, y - 25)
                self.resize(w, h)
            super(Main, self).keyPressEvent(event)

        def mousePressEvent(self, event):
            self.startpos = event.position()
            super(Main, self).mousePressEvent(event)

        def mouseMoveEvent(self, event):
            x = event.position().x() - self.startpos.x() + self.x()
            y = event.position().y() - self.startpos.y() + self.y()
            screen = self.screen().availableGeometry()
            x = max(screen.x(), x)
            x = min(x, screen.width() + screen.x() - self.width())
            y = max(screen.y(), y)
            y = min(y, screen.height() + screen.y() - self.height())
            self.move(x, y)
            super(Main, self).mouseMoveEvent(event)

        def showEvent(self, event):
            self.updateScreen()
            super(Main, self).showEvent(event)

    app = QApplication(sys.argv)
    image = Main()
    image.show()
    sys.exit(app.exec())
