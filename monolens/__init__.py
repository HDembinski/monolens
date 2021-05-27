__version__ = "0.3.0"


def main():
    from PySide6.QtWidgets import QApplication
    from .widget import Widget
    import sys

    app = QApplication(sys.argv)
    image = Widget()
    image.show()
    sys.exit(app.exec())
