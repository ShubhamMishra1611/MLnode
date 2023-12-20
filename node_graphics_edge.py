from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from node_socket import *

EDGE_CP_BOUNDINESS = 100

class Qgraphics_edge(QGraphicsPathItem):
    def __init__(self, edge, parent = None):
        super().__init__(parent)

        self._color = QColor('#001000')
        self._color_selected = QColor('#00ff00')

        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)
        self._pen_dragging = QPen(self._color)
        self._pen_dragging.setStyle(Qt.DashLine)
        self.edge = edge
        self._pen.setWidthF(2.0)
        self._pen_selected.setWidthF(2.0)
        self._pen_dragging.setWidthF(2.0)

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

        if self.edge.end_socket is None:
            painter.setPen(self._pen_dragging if not self.isSelected() else self._pen_selected)
        else:
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
        dist = (d[0] - s[0]) * 0.5
        cpx_s = +dist
        cpx_d = -dist
        cpy_s = 0
        cpy_d = 0

        sspos = self.edge.start_socket.position

        if (s[0] > d[0] and sspos in (RIGHT_TOP, RIGHT_BOTTOM)) or (s[0] < d[0] and sspos in (LEFT_BOTTOM, LEFT_TOP)):
            cpx_d *= -1
            cpy_s *= -1

            # if (s[1] - d[1]) != 0:
            #     cpy_d = ((s[1]-d[1])/abs(s[1]-d[1]))
            # else:
            #     cpy_d = 0.00001
             

        path = QPainterPath(QPointF(self.position_source[0], self.position_source[1]))
        path.cubicTo(
            s[0] + cpx_s, s[1] + cpy_s, d[0] + cpx_d, d[1] + cpy_d, self.position_destination[0], self.position_destination[1]
        )
        self.setPath(path)

