__version__ = "0.2.0"


def main():
    from PySide6.QtWidgets import QApplication
    from .main import Main
    import sys

    app = QApplication(sys.argv)
    image = Main()
    image.show()
    sys.exit(app.exec())
