from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Qgraphics_edge(QGraphicsPathItem):
    def __init__(self, edge, parent = None):
        super().__init__(parent)

        self._color = QColor('#001000')
        self._color_selected = QColor('#00ff00')

        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)
        self.edge = edge
        self._pen.setWidthF(2.0)
        self._pen_selected.setWidthF(2.0)

        self.setZValue(-1) # lets see

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.position_source = [0,0]
        self.position_destination = [200, 100]

    def set_source(self, x, y):
        self.position_source = [x, y]
    def set_destination(self, x, y):
        self.position_destination = [x, y]

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget = None) -> None:
        self.update_path()

        painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    def update_path():
        raise NotImplemented("This method has to be overridden in the child class")
    

class QGraphics_edge_direct(Qgraphics_edge):
    def update_path(self):
        path = QPainterPath(QPointF(self.position_source[0], self.position_source[1]))
        path.lineTo(self.position_destination[0], self.position_destination[1])
        self.setPath(path)

class QGraphics_edge_bezier(Qgraphics_edge):
    def update_path(self):
        s = self.position_source
        d = self.position_destination
        dist = abs(d[0] - s[0]) * 0.5
        path = QPainterPath(QPointF(self.position_source[0], self.position_source[1]))
        path.cubicTo(
            s[0] + dist, s[1], d[0] - dist, d[1], self.position_destination[0], self.position_destination[1]
        )
        self.setPath(path)

