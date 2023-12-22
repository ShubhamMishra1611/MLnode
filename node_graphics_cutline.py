from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QStyleOptionGraphicsItem, QWidget

class Q_Cutline(QGraphicsItem):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.line_points = []
        self._pen = QPen(Qt.white)
        self._pen.setWidthF(1.5)
        self._pen.setDashPattern([3, 3])

        self.setZValue(2)

    def boundingRect(self):
        return QRectF(0, 0, 1, 1)
    
    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = None) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(self._pen)
        poly = QPolygonF(
            self.line_points
        )
        painter.drawPolyline(poly)
    
