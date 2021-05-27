from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QGuiApplication, QImage, QPainter, QPen
from .util import clip


class Widget(QWidget):
    _screen = None

    def __init__(self):
        QWidget.__init__(self)
        for flag in (
            Qt.FramelessWindowHint,
            Qt.WindowStaysOnTopHint,
        ):
            self.setWindowFlag(flag)
        self.setAttribute(Qt.WA_OpaquePaintEvent)

        self.updateScreen()
        self._timer = QTimer(self)
        self._timer.setInterval(200)
        self._timer.timeout.connect(self.updateScreen)

    def updateScreen(self):
        screen = QGuiApplication.primaryScreen()
        wh = self.windowHandle()
        if wh:
            screen = wh.screen()
        if not screen:
            return
        image = screen.grabWindow(0).toImage()
        image = image.convertToFormat(QImage.Format_Grayscale8)
        if self._screen is not None:
            # use new screenshot for parts of screen not overlapping with window
            p = QPainter(image)
            margin = 50  # heuristic
            x = max(0, self.x() - margin)
            y = max(0, self.y() - margin)
            w = min(self.width() + 2 * margin, image.width())
            h = min(self.height() + 2 * margin, image.height())
            p.drawImage(x, y, self._screen, x, y, w, h)
            p.end()
        self._screen = image

    def enterEvent(self, event):
        self.updateScreen()
        self._timer.start()
        super(Widget, self).eventEvent(event)

    def leaveEvent(self, event):
        self._timer.stop()
        super(Widget, self).leaveEvent(event)

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
        self.update()
        super(Widget, self).resizeEvent(event)

    def moveEvent(self, event):
        self.update()
        super(Widget, self).moveEvent(event)

    def keyPressEvent(self, event):
        key = event.key()
        if key in (Qt.Key_Escape, Qt.Key_Q):
            self.close()
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
        self._startpos = event.position()
        super(Widget, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        x = event.position().x() - self._startpos.x() + self.x()
        y = event.position().y() - self._startpos.y() + self.y()
        self.move(*self._clipXY(x, y))
        super(Widget, self).mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.close()
        super(Widget, self).mouseDoubleClickEvent(event)

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
