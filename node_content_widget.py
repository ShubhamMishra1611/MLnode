import typing
from collections import OrderedDict
from node_serializable import Serializable

from PyQt5 import QtCore
from PyQt5.QtGui import QFocusEvent, QKeyEvent
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget

class QNode_content_widget(QWidget, Serializable):
    def __init__(self, node,  parent=None) -> None:
        super().__init__(parent)
        self.node = node
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self.wdg_label = QLabel("Random things ")
        self.layout.addWidget(self.wdg_label)
        self.layout.addWidget(Q_TextEdit("Scibdi duph"))

    def setEditingFlag(self, value):
        # self.node.scene.grscene.views()[0].editing_flag = value
        self.node.scene.getView().editingFlag = value

    def serialize(self):
        return OrderedDict([

        ])

    def deserialize(self, data, hashmap={}):
        return True


class Q_TextEdit(QTextEdit):

    def focusInEvent(self, e: QFocusEvent) -> None:
        self.parentWidget().setEditingFlag(True)
        super().focusInEvent(e)
    
    def focusOutEvent(self, e: QFocusEvent) -> None:
        self.parentWidget().setEditingFlag(False)
        super().focusOutEvent(e)
