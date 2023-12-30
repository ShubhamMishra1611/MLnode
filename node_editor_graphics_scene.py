import math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush
from PyQt5.QtCore import *


class Node_Editor_Graphics_Scene(QGraphicsScene):
    itemSelected = pyqtSignal()
    itemsDeselected = pyqtSignal()

    def __init__(self, scene, parent = None):
        super().__init__(parent)
        self.grid_size = 50
        self.scene = scene
        self._back_color = QColor("#393939")
        self._color_light = QColor("#2f2f2f")
        self._color_dark = QColor("#292929")
        self._color_brush_light = QBrush(self._color_light)
        self._color_brush_dark = QBrush(self._color_dark)
        self._pen_color_light = QPen(self._color_light)
        self._pen_color_dark = QPen(self._color_dark)
        self._pen_color_dark.setWidth(5)
        self._pen_color_light.setWidth(5)
        
        # set the background color
        self.setBackgroundBrush(self._back_color)

    def set_scene(self, width, height):
        # set a rectangular 
        self.setSceneRect(
            -width//2,#0
            -height//2,#0
            width,
            height
        )


    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        super().drawBackground(painter, rect)
        left = int(math.floor(rect.left()))
        top = int(math.floor(rect.top()))
        right = int(math.ceil(rect.right()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left-(left%self.grid_size)
        first_top = top-(top%self.grid_size)

        dot_radius = 2.5
        

        for y in range(first_top, bottom, self.grid_size):
            for x in range(first_left, right, self.grid_size):
                dot = QGraphicsEllipseItem(x, y, dot_radius, dot_radius)
                dot.setPen(self._pen_color_light)
                dot.setBrush(self._color_brush_light)
                painter.drawEllipse(dot.rect())




# if __name__ == "__main__":
#     node_editor_scene = Node_Editor_Graphics_Scene()
