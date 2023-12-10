import typing
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGraphicsTextItem

class QgraphicsNode(QGraphicsItem):
    def __init__(self, node, title = "NodeGraphicsItem", parent=None) -> None:
        super().__init__(parent)
        self.title = title
        self._title_color = Qt.white
        self._title_font = QFont("Ubuntu", 10)
        self.initTitle()
        self.initUI()

    def initUI(self):
        # self.setFlag(QGraphicsItem.ItemIsSelectable)
        # self.setFlag(QGraphicsItem.ItemIsMovable)
        pass

    def initTitle(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        # self.title_item.setPos(self._padding, 0)
        # self.title_item.setTextWidth(
        #     self.width
        #     - 2 * self._padding
        # )



