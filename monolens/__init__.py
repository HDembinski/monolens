from ._version import version as __version__  # noqa


def main():
    from PySide6 import QtWidgets, QtCore
    from .lens import Lens
    from .util import DEBUG
    import sys
    import signal

    QtCore.QCoreApplication.setOrganizationName("Monolens")
    QtCore.QCoreApplication.setApplicationName("Monolens")

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtWidgets.QApplication(sys.argv)

    settings = QtCore.QSettings()

    if "--reset" in app.arguments()[1:]:
        settings.clear()

    # TODO would be great to read this from README.md
    print(
        """Welcome to Monolens

Monolens allows you to view part of your screen in grayscale.

Usage

- Drag the lens around by holding a Mouse button down inside the window
- To quit, press Escape, Q, or double click on the lens
- Resize the lens by pressing up, down, left, right
- Press Tab to switch between monochrome view and simulated
  protanopia, deuteranopia, tritanopia
- To move the lens to another screen, press M

On OSX, you need to give Monolens permission to make screenshots, which is safe.
"""
    )

    if DEBUG:
        print("settings:")
        for key in settings.allKeys():
            value = settings.value(key)
            print(f"  {key}: {value}")

    lens = Lens()
    lens.show()
    sys.exit(app.exec())
