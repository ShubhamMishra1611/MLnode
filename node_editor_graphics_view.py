from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import QPainter, QWheelEvent, QMouseEvent
from PyQt5.QtCore import Qt, QEvent

class Node_Editor_Graphics_View(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(parent)
        self.scene = scene
        self.initUI()
        self.setScene(self.scene)

        self.zoom_in_factor = 1.25
        self.zoom = 10
        self.zoom_step = 1
        self.zoom_clamp = False
        self.zoom_range = [6, 12]

    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def wheelEvent(self, event: QWheelEvent) -> None:
        zoom_out_factor = 1/self.zoom_in_factor

        #storing the position
        old_position = self.mapToScene(event.pos())

        if event.angleDelta().y() >0:
            zoom_factor = self.zoom_in_factor
            self.zoom += self.zoom_step
        else:
            zoom_factor = zoom_out_factor
            self.zoom -= self.zoom_step
        self.zoom_clamp = False
        if not (self.zoom_range[1]>=self.zoom and self.zoom>=self.zoom_range[0]):
            self.zoom_clamp = True
            if self.zoom>=self.zoom_range[1]:self.zoom = self.zoom_range[1]
            if self.zoom<=self.zoom_range[0]:self.zoom = self.zoom_range[0]

        print(self.zoom)
        if not self.zoom_clamp:
            self.scale(zoom_factor, zoom_factor)

        new_pos = self.mapToScene(event.pos())
        delta = new_pos-old_position
        self.translate(delta.x(), delta.y())

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button()==Qt.MiddleButton:
            self.MiddleMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.RightMouseButtonPress(event)
        elif event.button == Qt.LeftButton:
            self.LeftMouseButtonPress(event)
        else:
            super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button()==Qt.MiddleButton:
            self.MiddleMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.RightMouseButtonRelease(event)
        elif event.button == Qt.LeftButton:
            self.LeftMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def MiddleMouseButtonPress(self, event:QMouseEvent):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(), 
                                   Qt.LeftButton, Qt.NoButton, event.modifiers() )
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, 
                                event.buttons()|Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def MiddleMouseButtonRelease(self, event:QMouseEvent):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)

    def RightMouseButtonPress(self, event:QMouseEvent):
        return super.mousePressEvent(event)
    def LeftMouseButtonPress(self, event:QMouseEvent):
        return super.mousePressEvent(event)
    def RightMouseButtonRelease(self, event:QMouseEvent):
        return super.mouseReleaseEvent(event)
    def LeftMouseButtonRelease(self, event:QMouseEvent):
        return super.mouseReleaseEvent(event)


        

    
