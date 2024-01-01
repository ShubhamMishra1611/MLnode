import typing
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsProxyWidget, QGraphicsSceneMouseEvent
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QFont, QPen, QColor, QBrush, QPainterPath
from PyQt5.QtWidgets import QGraphicsTextItem

class QgraphicsNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        super().__init__(parent)

        self.node = node
        self.content = self.node.content

        self._was_moved = False
        self._last_selected_state = False

        self.initSizes()
        self.initAssets()
        self.initUI()



    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

        # init title
        self.initTitle()
        self.title = self.node.title

        self.initcontent()


    def initSizes(self):
        self.width = 180
        self.height = 240
        # self.edge_roundness = 10.0
        self.title_height = 24.0
        # self._padding = 4.0
        self.edge_roundness = 10.0
        self.edge_padding = 10.0
        self.title_horizontal_padding = 4.0
        self.title_vertical_padding = 4.0


    def initAssets(self):
        self._title_color = Qt.white
        self._title_font = QFont("Ubuntu", 10)


        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_selected = QPen(QColor("#FFFFA637"))

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))


    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mouseMoveEvent(event)

        for node in self.scene().scene.nodes:
            if node.graphical_node.isSelected():
                node.update_connected_edges()

        self._was_moved = True

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mouseReleaseEvent(event)

        if self._was_moved:
            self._was_moved = False
            self.node.scene.history.store_history("Node moved")

        if self._last_selected_state != self.isSelected():
            self.node.scene.resetLastSelectedStates()
            self._last_selected_state = self.isSelected()
            self.node.scene._last_selected_items = self.node.scene.getSelectedItems()
            return 
        if self._last_selected_state != self.isSelected() or self.node.scene._last_selected_items != self.node.scene.getSelectedItems():
            self.node.scene.resetLastSelectedStates()
            self._last_selected_state = self.isSelected()
            self.onSelected()

    
    def onSelected(self):
        self.node.scene.grscene.itemSelected.emit()


    @property
    def title(self): return self._title
    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)
        
    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()


    def initTitle(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self.title_horizontal_padding, 0)
        self.title_item.setTextWidth(
            self.width
            - 2 * self.title_horizontal_padding
        )

    def initcontent(self):
        self.grContent = QGraphicsProxyWidget(self)
        self.content.setGeometry(int(self.edge_padding), int(self.title_height + self.edge_padding),
                                 int(self.width - 2*self.edge_padding), int(self.height - 2*self.edge_padding-self.title_height))
        self.grContent.setWidget(self.content)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0,0, self.width, self.title_height, self.edge_roundness, self.edge_roundness)
        path_title.addRect(0, self.title_height - self.edge_roundness, self.edge_roundness, self.edge_roundness)
        path_title.addRect(self.width - self.edge_roundness, self.title_height - self.edge_roundness, self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())


        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_roundness, self.edge_roundness)
        path_content.addRect(0, self.title_height, self.edge_roundness, self.edge_roundness)
        path_content.addRect(self.width - self.edge_roundness, self.title_height, self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())


        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_roundness, self.edge_roundness)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())



