from PySide6 import QtWidgets, QtCore, QtGui
from pathlib import Path
import re


class Intro(QtWidgets.QWidget):

    closed = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.setContentsMargins(50, 50, 50, 50)

        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

        with open(Path(__file__).parent / ".." / ".." / "README.md") as f:
            m = re.search("<!-- usage begin -->\n(.+?)\n<!--", f.read(), re.DOTALL)
            usage = m.group(1).split("\n-")
        usage = "".join(f"<li>{x}</li>" for x in usage)

        tx = f"""<h1 align="center">Welcome to Monolens</h1>
        <p>Monolens allows you to view part of your screen in grayscale.</p>
        <h2>Usage</h2>
        <ul>
        {usage}
        </ul>
        <br>
        """

        font = QtGui.QFont()
        font.setPointSize(16)
        text = QtWidgets.QLabel(tx)
        text.setFont(font)
        button = QtWidgets.QPushButton("Start")
        checkbox = QtWidgets.QCheckBox("Do not show this again")

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(text)
        layout2 = QtWidgets.QHBoxLayout()
        layout2.addWidget(checkbox)
        layout2.addWidget(button)
        layout.addLayout(layout2)
        button.clicked.connect(self.close)
        checkbox.toggled.connect(
            lambda checked: QtCore.QSettings().setValue("show_intro", str(not checked))
        )

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)
