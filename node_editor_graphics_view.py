from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import QKeyEvent, QPainter, QWheelEvent, QMouseEvent
from PyQt5.QtCore import Qt, QEvent
from node_graphics_socket import Qgraphics_socket
from node_graphics_edge import Qgraphics_edge
from node_edge import Edge, EDGE_BEZIER, EGDE_DIRECT

MODE_NOOP = 1
MODE_EDGE_DRAG = 2
EDGE_DRAG_START_THRESHOLD = 10
DEBUG = True

class Node_Editor_Graphics_View(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(parent)
        self.scene = scene
        self.initUI()
        self.setScene(self.scene)

        self.mode = MODE_NOOP
        self.editing_flag = False

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
        self.setDragMode(QGraphicsView.RubberBandDrag)

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

        # print(self.zoom)
        if not self.zoom_clamp:
            self.scale(zoom_factor, zoom_factor)

        new_pos = self.mapToScene(event.pos())
        delta = new_pos-old_position
        self.translate(delta.x(), delta.y())

    def mousePressEvent(self, event) -> None:
        if event.button()==Qt.MiddleButton:
            self.MiddleMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.RightMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.LeftMouseButtonPress(event)
        else:
            super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button()==Qt.MiddleButton:
            self.MiddleMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.RightMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
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
        super().mousePressEvent(event)

        item = self.get_item_at_click(event)
        if DEBUG:
            if isinstance(item, Qgraphics_edge): print("DEBUG:: RMB, ", item.edge, 'connecting sockets as', item.edge.start_socket, '<--->', item.edge.end_socket) 
            if type(item) is Qgraphics_socket: print("DEBUG:: RMB, ", item.socket,  'has edge', item.socket.edge)
            if item is None:
                print('SCENE: ')
                print(' Nodes: ')
                for node in self.scene.scene.nodes: print('      ', node)
                print(' Edges: ')
                for edge in self.scene.scene.edges: print('      ', edge)

    def RightMouseButtonRelease(self, event:QMouseEvent):
        super().mouseReleaseEvent(event)

    def LeftMouseButtonPress(self, event:QMouseEvent):
        item = self.get_item_at_click(event)
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())
        if DEBUG: print(f'LMB click on {item}, {self.debug_modifiers(event)}')
        if type(item) is Qgraphics_socket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edge_drag_start(item)
                return 
            
        if self.mode == MODE_EDGE_DRAG:
            res = self.edge_drag_end(item)
            if res: return
        super().mousePressEvent(event)

    def LeftMouseButtonRelease(self, event:QMouseEvent):
        item  = self.get_item_at_click(event)
        if self.mode == MODE_EDGE_DRAG:
            # if dist between click and release is off
            if  self.dist_between_click_and_release_is_off(event):
                res = self.edge_drag_end(item)
                if res: return
        super().mouseReleaseEvent(event)


    def mouseMoveEvent(self, event) -> None:
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.drag_edge.graphical_edge.set_destination(pos.x(), pos.y())
            self.drag_edge.graphical_edge.update()
        super().mouseMoveEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Delete:
            if not self.editing_flag:
                self.delete_selected()
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def delete_selected(self):
        for item in self.scene.selectedItems():
            if isinstance(item, Qgraphics_edge):
                item.edge.remove()
            elif hasattr(item, 'node'):
                item.node.remove()
    
    def dist_between_click_and_release_is_off(self, event):
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        distance = dist_scene.x()*dist_scene.x() + dist_scene.y()*dist_scene.y()
        return distance > EDGE_DRAG_START_THRESHOLD*EDGE_DRAG_START_THRESHOLD
    
    def edge_drag_start(self, item):
        if DEBUG: print('View::edge_drag_start ~ start dragging edge')
        if DEBUG: print('View::edge_drag_start ~    assign start socket')
        self.previous_edge = item.socket.edge
        self.last_start_socket = item.socket
        self.drag_edge = Edge(self.scene.scene, item.socket, None, EDGE_BEZIER)
        if DEBUG: print('View::edge_drag_start ~ ', self.drag_edge)

    def edge_drag_end(self, item):
        self.mode = MODE_NOOP
        if type(item) is Qgraphics_socket:
            if item.socket != self.last_start_socket:
                if item.socket.has_edge():
                    item.socket.edge.remove()
                if DEBUG:print('View::edge_drag_end ~   assign end socket', item.socket)
                if self.previous_edge is not None:
                    self.previous_edge.remove()
                    if DEBUG:print('View::edge_drag_end ~   previous edge removed', item.socket)
                self.drag_edge.start_socket = self.last_start_socket
                self.drag_edge.end_socket = item.socket
                self.drag_edge.start_socket.set_connected_edge(self.drag_edge)
                self.drag_edge.end_socket.set_connected_edge(self.drag_edge)
                if DEBUG: print('View::edge_drag_end ~ assigned start and end socket to drag edge')
                self.drag_edge.update_positions()
                # if self.drag_edge.end_socket == self.drag_edge.start_socket:
                #     if DEBUG: print('View::edge_drag_end ~ edge assigned to same socket... removed')
                #     self.drag_edge.remove()
                return True
        if DEBUG:print('View::edge_drag_end ~ End of dragging edge')
        self.drag_edge.remove()
        self.drag_edge = None
        if DEBUG:print('View::edge_drag_end ~ about to set socket to previous edge', self.previous_edge)
        if self.previous_edge is not None:
            self.previous_edge.start_socket.edge = self.previous_edge
        if DEBUG:print('View::edge_drag_end ~ Everything done')
        
        return False

    def get_item_at_click(self, event):
        pos = event.pos()
        item = self.itemAt(pos)
        return item
    
    def debug_modifiers(self, event):
        out = 'MODS:'
        if event.modifiers() & Qt.ShiftModifier: out += 'SHIFT'
        if event.modifiers() & Qt.AltModifier: out += 'ALT'
        if event.modifiers() & Qt.ControlModifier: out += 'CTRL'
        return out


        

    
