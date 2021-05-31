from PySide6 import QtWidgets, QtCore, QtGui


class Intro(QtWidgets.QWidget):

    closed = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.setContentsMargins(50, 50, 50, 50)

        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

        sgeo = self.screen().availableGeometry()
        w = sgeo.width()
        h = sgeo.height()
        self.setGeometry(0.6 * w, 0.25 * h, 0.35 * w, 0.5 * h)

        # TODO would be great to read this list from README
        tx = """<h1 align="center">Welcome to Monolens</h1>
        <p>Monolens allows you to view part of your screen in grayscale.</p>
        <h2>Usage</h2>
        <ul>
            <li>Drag the lens around by holding a Mouse button down inside the window</li>
            <li>To quit, press Escape, Q, or double click on the lens</li>
            <li>Resize the lens by pressing up, down, left, right</li>
            <li>Press Tab to switch between monochrome view and simulated<br>
                protanopia, deuteranopia, tritanopia</li>
            <li>To move the lens to another screen, press M</li>
        </ul>
        <br>
        <p>
            On OSX, you need to give Monolens permission to make screenshots, which is
            safe.
        </p>
        """

        font = QtGui.QFont()
        font.setPointSize(16)
        text = QtWidgets.QLabel(tx)
        text.setFont(font)
        button = QtWidgets.QPushButton("Close")
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
