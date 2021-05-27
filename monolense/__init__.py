__version__ = "0.1.1"


def main():
    from PySide6.QtWidgets import QApplication
    from .main import Main
    import sys

    app = QApplication(sys.argv)
    image = Main()
    image.show()
    sys.exit(app.exec())
