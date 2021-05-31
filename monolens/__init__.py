from ._version import version as __version__  # noqa


def main():
    from PySide6 import QtWidgets, QtCore
    from .lens import Lens
    from .util import DEBUG
    import sys
    import signal
    import re

    if sys.version_info < (3, 9):
        import importlib_resources
    else:
        import importlib.resources as importlib_resources

    QtCore.QCoreApplication.setOrganizationName("Monolens")
    QtCore.QCoreApplication.setApplicationName("Monolens")

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtWidgets.QApplication(sys.argv)

    settings = QtCore.QSettings()

    if "--reset" in app.arguments()[1:]:
        settings.clear()

    pkg = importlib_resources.files("monolens")
    with open(pkg / "README.md") as f:
        tx = f.read()
        tag = "<!-- {0} begin -->\n(.+?)\n<!-- {0} end -->"
        m = re.search(tag.format("description"), tx, re.DOTALL)
        assert m
        print(m.group(1))
        print("\nUsage:\n")
        m = re.search(tag.format("usage"), tx, re.DOTALL)
        assert m
        print(m.group(1))

    if DEBUG:
        print("settings:")
        for key in settings.allKeys():
            value = settings.value(key)
            print(f"  {key}: {value}")

    lens = Lens()
    lens.show()
    sys.exit(app.exec())
