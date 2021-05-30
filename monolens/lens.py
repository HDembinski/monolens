from PySide6 import QtWidgets, QtCore, QtGui
from . import util


class Lens(QtWidgets.QWidget):
    _screenshot = None
    _converted = None

    def __init__(self):
        super().__init__()
        for flag in (
            QtCore.Qt.FramelessWindowHint,
            QtCore.Qt.WindowStaysOnTopHint,
        ):
            self.setWindowFlag(flag)
        for flag in (
            QtCore.Qt.WA_OpaquePaintEvent,
            QtCore.Qt.WA_NoSystemBackground,
        ):
            self.setAttribute(flag)
        self._updateScreenshot(self.screen())

    def paintEvent(self, event):
        sgeo = self.screen().geometry()
        wgeo = self.geometry()
        dpr = self.devicePixelRatio()
        x = wgeo.x() - sgeo.x()
        y = max(0, wgeo.y() - sgeo.y())
        w = wgeo.width()
        h = wgeo.height()
        if util.DEBUG:
            print("paint", x, y, w, h)
        p = QtGui.QPainter(self)
        p.drawImage(0, 0, self._converted, x * dpr, y * dpr, w * dpr, h * dpr)
        p.setPen(QtGui.QPen(QtCore.Qt.white, 3))
        p.drawRect(1, 1, w - 2, h - 2)
        p.end()
        super().paintEvent(event)

    def resizeEvent(self, event):
        if util.DEBUG < 2:
            self._updateScreenshot(self.screen())
        self.repaint(0, 0, -1, -1)  # better than update() on OSX
        super().resizeEvent(event)

    def moveEvent(self, event):
        if util.DEBUG < 2:
            self._updateScreenshot(self.screen())
        self.repaint(0, 0, -1, -1)  # better than update() on OS
        super().moveEvent(event)

    def keyPressEvent(self, event):
        key = event.key()
        if key in (QtCore.Qt.Key_Escape, QtCore.Qt.Key_Q):
            self.close()
        elif key == QtCore.Qt.Key_S:
            self._moveToNextScreen()
        elif key == QtCore.Qt.Key_Left:
            x = self.x() + 25
            y = self.y()
            w = max(50, self.width() - 50)
            h = self.height()
            x, y, w, h = self._clipAll(x, y, w, h)
            self.move(x, y)
            self.resize(w, h)
        elif key == QtCore.Qt.Key_Right:
            x = self.x() - 25
            y = self.y()
            w = self.width() + 50
            h = self.height()
            x, y, w, h = self._clipAll(x, y, w, h)
            self.move(x, y)
            self.resize(w, h)
        elif key == QtCore.Qt.Key_Down:
            x = self.x()
            y = self.y() + 25
            w = self.width()
            h = max(50, self.height() - 50)
            x, y, w, h = self._clipAll(x, y, w, h)
            self.move(x, y)
            self.resize(w, h)
        elif key == QtCore.Qt.Key_Up:
            x = self.x()
            y = self.y() - 25
            w = self.width()
            h = self.height() + 50
            x, y, w, h = self._clipAll(x, y, w, h)
            self.move(x, y)
            self.resize(w, h)
        super().keyPressEvent(event)

    def mousePressEvent(self, event):
        self._startpos = event.position()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        x = event.position().x() - self._startpos.x() + self.x()
        y = event.position().y() - self._startpos.y() + self.y()
        self.move(*self._clipXY(x, y))
        super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.close()
        super().mouseDoubleClickEvent(event)

    def _updateScreenshot(self, screen):
        if not screen:
            return
        if util.DEBUG:
            print("_updateScreenshot", screen.availableGeometry())
        pix = screen.grabWindow(0)
        if (
            not self._screenshot
            or self._screenshot.width() != pix.width()
            or self._screenshot.height() != pix.height()
        ):
            self._screenshot = pix.toImage()
            self._converted = QtGui.QImage(
                pix.width(), pix.height(), QtGui.QImage.Format_RGB32
            )
        else:
            # override lens with old pixels from previous screenshot
            p = QtGui.QPainter(self._screenshot)
            margin = 100  # heuristic
            sgeo = screen.geometry()
            wgeo = self.geometry()
            dpr = self.devicePixelRatio()
            x1 = max(0, wgeo.x() - sgeo.x() - margin)
            y1 = max(0, wgeo.y() - sgeo.y() - margin)
            x2 = x1 + min(wgeo.width() + 2 * margin, sgeo.width())
            y2 = y1 + min(wgeo.height() + 2 * margin, sgeo.height())
            # why first two arguments must be x, y instead of x * dpr, y * dpr?
            if util.DEBUG:
                print("_updateScreenshot", x1, y1, x2, y2)
            # region left of window
            if x1 > 0:
                p.drawPixmap(0, 0, pix, 0, 0, x1 * dpr, -1)
            # region right of window
            if x2 < sgeo.width():
                p.drawPixmap(x2, 0, pix, x2 * dpr, 0, -1, -1)
            # region above window
            if y1 > 0:
                p.drawPixmap(x1, 0, pix, x1 * dpr, 0, (x2 - x1) * dpr, y1 * dpr)
            # region below window
            if y2 < sgeo.height():
                p.drawPixmap(x1, y2, pix, x1 * dpr, y2 * dpr, (x2 - x1) * dpr, -1)
            p.end()
        self._updateConverted()

    def _updateConverted(self):
        # util.grayscale(self._converted, self._screenshot)
        util.colorblindness(self._converted, self._screenshot, 0)

    def _clipXY(self, x, y):
        screen = self.screen().availableGeometry()
        x = util.clip(x, screen.x(), screen.width() + screen.x() - self.width())
        y = util.clip(y, screen.y(), screen.height() + screen.y() - self.height())
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

    def _moveToNextScreen(self):
        # discover on which screen we are
        screens = QtGui.QGuiApplication.screens()
        for iscr, scr in enumerate(screens):
            sgeo = scr.geometry()
            if sgeo.contains(self.geometry()):
                break
        # move window to screen
        nscr = len(screens)
        iscr = (iscr + 1) % nscr
        scr = screens[iscr]
        self._screenshot = None
        self._updateScreenshot(scr)
        ageo = scr.availableGeometry()
        x = ageo.center().x() - self.width() // 2
        y = ageo.center().y() - self.height() // 2
        self.move(x, y)
