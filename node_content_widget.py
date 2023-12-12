import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget

class QNode_content_widget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self.wdg_label = QLabel("Random things ")
        self.layout.addWidget(self.wdg_label)
        self.layout.addWidget(QTextEdit("Scibdi duph "))
