__version__ = "0.4.2"


def main():
    from PySide6.QtWidgets import QApplication
    from .widget import Widget
    import sys
    import signal

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    image = Widget()
    image.show()
    sys.exit(app.exec())
