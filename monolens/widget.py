from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPainter, QPen
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

    def updateScreen(self):
        screen = self.screen()
        if not screen:
            return
        image = screen.grabWindow(0).toImage()
        image = image.convertToFormat(QImage.Format_Grayscale8)
        if self._screen:
            # use new screenshot for parts of screen not overlapping with window
            p = QPainter(image)
            margin = 100  # heuristic
            wgeo = self.geometry()
            sgeo = screen.geometry()
            dpr = self.devicePixelRatio()
            x = max(0, wgeo.x() - sgeo.x() - margin)
            y = max(0, wgeo.y() - sgeo.y() - margin)
            w = min(wgeo.width() + 2 * margin, sgeo.width())
            h = min(wgeo.height() + 2 * margin, sgeo.height())
            # why first two arguments must be x, y instead of x * dpr, y * dpr?
            p.drawImage(x, y, self._screen, x * dpr, y * dpr, w * dpr, h * dpr)
            p.end()
        self._screen = image

    def paintEvent(self, event):
        sgeo = self.screen().geometry()
        wgeo = self.geometry()
        dpr = self.devicePixelRatio()
        x = wgeo.x() - sgeo.x()
        y = max(0, wgeo.y() - sgeo.y())
        w = wgeo.width()
        h = wgeo.height()
        p = QPainter(self)
        p.drawImage(0, 0, self._screen, x * dpr, y * dpr, w * dpr, h * dpr)
        p.setPen(QPen(Qt.white, 3))
        p.drawRect(1, 1, w - 2, h - 2)
        p.end()
        super(Widget, self).paintEvent(event)

    def resizeEvent(self, event):
        self.updateScreen()
        self.update()
        super(Widget, self).resizeEvent(event)

    def moveEvent(self, event):
        self.updateScreen()
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
