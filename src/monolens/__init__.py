from ._version import version as __version__  # noqa


def main():
    from PySide6 import QtWidgets, QtCore
    from .lens import Lens
    from .intro import Intro
    from .util import DEBUG
    import sys
    import signal

    QtCore.QCoreApplication.setOrganizationName("Monolens")
    QtCore.QCoreApplication.setApplicationName("Monolens")

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtWidgets.QApplication(sys.argv)
    lens = Lens()
    settings = QtCore.QSettings()
    if DEBUG:
        print("settings:")
        for key in settings.allKeys():
            value = settings.value(key)
            print(f"  {key}: {value}")
    if settings.value("show_intro", "True") == "True":
        intro = Intro()
        intro.show()
        intro.closed.connect(lens.show)
    else:
        lens.show()
    sys.exit(app.exec())
