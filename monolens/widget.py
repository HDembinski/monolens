from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QGuiApplication, QImage, QPainter, QPen
from .util import clip


class Widget(QWidget):
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
        screen = self.screen().geometry()
        x = self.x() - screen.x()
        y = max(0, self.y() - screen.y())
        w = self.width()
        h = self.height()
        dpr = self.devicePixelRatio()

        p = QPainter(self)
        p.drawImage(0, 0, self._screen, x * dpr, y * dpr, w * dpr, h * dpr)
        p.setPen(QPen(Qt.white, 3))
        p.drawRect(0, 0, w, h)
        p.end()
        super(Widget, self).paintEvent(event)

    def resizeEvent(self, event):
        self.refresh()
        super(Widget, self).resizeEvent(event)

    def moveEvent(self, event):
        self.refresh()
        super(Widget, self).moveEvent(event)

    def keyPressEvent(self, event):
        key = event.key()
        if key in (Qt.Key_Escape, Qt.Key_Q):
            self.close()
        elif key == Qt.Key_Space:
            self.hide()
            QTimer.singleShot(0, self.show)
        elif key == Qt.Key_Left:
            x = self.x() + 25
            y = self.y()
            w = max(50, self.width() - 50)
            h = self.height()
            x, y, w, h = self._clipAll(x, y, w, h)
            self.move(x, y)
            self.resize(w, h)
        elif key == Qt.Key_Right:
            x = self.x() - 25
            y = self.y()
            w = self.width() + 50
            h = self.height()
            x, y, w, h = self._clipAll(x, y, w, h)
            self.move(x, y)
            self.resize(w, h)
        elif key == Qt.Key_Down:
            x = self.x()
            y = self.y() + 25
            w = self.width()
            h = max(50, self.height() - 50)
            x, y, w, h = self._clipAll(x, y, w, h)
            self.move(x, y)
            self.resize(w, h)
        elif key == Qt.Key_Up:
            x = self.x()
            y = self.y() - 25
            w = self.width()
            h = self.height() + 50
            x, y, w, h = self._clipAll(x, y, w, h)
            self.move(x, y)
            self.resize(w, h)
        super(Widget, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        self.startpos = event.position()
        super(Widget, self).mousePressEvent(event)

    def _clipXY(self, x, y):
        screen = self.screen().availableGeometry()
        x = clip(x, screen.x(), screen.width() + screen.x() - self.width())
        y = clip(y, screen.y(), screen.height() + screen.y() - self.height())
        return x, y

    def _clipAll(self, x, y, w, h):
        screen = self.screen().availableGeometry()
        x1 = x
        x2 = x + w
        y1 = y
        y2 = y + h
        x1 = max(x1, screen.x())
        y1 = max(y1, screen.y())
        x2 = min(x2, screen.x() + screen.width())
        y2 = min(y2, screen.y() + screen.height())
        return x1, y1, x2 - x1, y2 - y1

    def mouseMoveEvent(self, event):
        x = event.position().x() - self.startpos.x() + self.x()
        y = event.position().y() - self.startpos.y() + self.y()
        self.move(*self._clipXY(x, y))
        super(Widget, self).mouseMoveEvent(event)

    def showEvent(self, event):
        self.updateScreen()
        super(Widget, self).showEvent(event)
