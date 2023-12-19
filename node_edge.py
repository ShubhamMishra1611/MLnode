from node_graphics_edge import *

EGDE_DIRECT = 1
EDGE_BEZIER = 2

class Edge:
    def __init__(self, scene, start_socket, end_socket, type_edge = EGDE_DIRECT) -> None:
        self.scene = scene
        self.start_socket = start_socket
        self.end_socket = end_socket

        self.start_socket.edge = self
        if self.end_socket is not None:
            self.end_socket.edge = self

        self.graphical_edge = QGraphics_edge_direct(self) if type_edge == EGDE_DIRECT else QGraphics_edge_bezier(self)

        self.update_positions()
        self.scene.grscene.addItem(self.graphical_edge)

    def update_positions(self):
        source_position = self.start_socket.get_socket_position()
        source_position[0] += self.start_socket.node.graphical_node.pos().x()
        source_position[1] += self.start_socket.node.graphical_node.pos().y()
        self.graphical_edge.set_source(*source_position)
        if self.end_socket is not None:
            end_position = self.end_socket.get_socket_position()
            end_position[0] += self.end_socket.node.graphical_node.pos().x()
            end_position[1] += self.end_socket.node.graphical_node.pos().y()
            self.graphical_edge.set_destination(*end_position)
        self.graphical_edge.update()


    def remove_from_socket(self):
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None

        self.start_socket = None
        self.end_socket = None

    def remove(self):
        self.remove_from_socket()
        self.scene.grscene.removeItem(self.graphical_edge)
        self.graphical_edge = None
        self.scene.removeEdge(self)