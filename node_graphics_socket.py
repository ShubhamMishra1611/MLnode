from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QGraphicsSceneMouseEvent

class Qgraphics_socket(QGraphicsItem):
    def __init__(self, socket, socket_type = 1):
        self.socket = socket
        super().__init__(socket.node.graphical_node)

        self.radius = 6
        self._outline_width = 1.0
        self._colors = [
            QColor("#74A662"),
            QColor("#FFFF7700"),
            QColor("#FF52E220"),
            QColor("#FFA86DB1"),
            QColor("#74A662"),
            QColor("#74A662")
        ]
        self._color_background = self._colors[socket_type]
        self._color_outline = QColor("#FF000000")

        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self._outline_width)
        self._brush = QBrush(self._color_background)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget = None) -> None:
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawEllipse(
            -self.radius,
            -self.radius,
            2*self.radius,
            2*self.radius
        )

    def boundingRect(self) -> QRectF:
        return QRectF(
            -self.radius - self._outline_width,
            -self.radius - self._outline_width,
            2*(self.radius + self._outline_width),
            2*(self.radius + self._outline_width)
        )
    
