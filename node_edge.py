from node_graphics_edge import *
from collections import OrderedDict
from node_serializable import Serializable


EGDE_DIRECT = 1
EDGE_BEZIER = 2

class Edge(Serializable):
    def __init__(self, scene, start_socket=None, end_socket=None, type_edge = EGDE_DIRECT) -> None:
        super().__init__()
        self.scene = scene
        self._start_socket = None
        self._end_socket = None
        self.start_socket = start_socket
        self.end_socket = end_socket
        self.edge_type = type_edge

        self.scene.add_edge(self)

    def __str__(self) -> str:
        return "<Edge %s>" % (hex(id(self)))
    
    def getOtherSocket(self, known_socket):
        return self.start_socket if known_socket == self.end_socket else self.end_socket

    @property
    def start_socket(self):return self._start_socket

    @start_socket.setter
    def start_socket(self, value):
        # if we were assigned to some socket before, delete us from the socket
        if self._start_socket is not None:
            self._start_socket.remove_edge(self)

        # assign new start socket
        self._start_socket = value
        if self.start_socket is not None:
            self.start_socket.add_edge(self)
    @property
    def end_socket(self):return self._end_socket

    @end_socket.setter
    def end_socket(self, value):
        # if we were assigned to some socket before, delete us from the socket
        if self._end_socket is not None:
            self._end_socket.remove_edge(self)

        # assign new end socket
        self._end_socket = value
        if self.end_socket is not None:
            self.end_socket.add_edge(self)
    

    @property
    def edge_type(self): return self._edge_type
    
    @edge_type.setter
    def edge_type(self, value):
        if hasattr(self, 'graphical_edge') and self.graphical_edge is not None:
            self.scene.grscene.removeItem(self.graphical_edge)

        self._edge_type = value
        if self.edge_type == EDGE_BEZIER:
            self.graphical_edge = QGraphics_edge_bezier(self)
        elif self.edge_type == EGDE_DIRECT:
            self.graphical_edge = QGraphics_edge_direct(self)
        else:
            self.graphical_edge = QGraphics_edge_bezier(self)

        self.scene.grscene.addItem(self.graphical_edge)

        if self.start_socket is not None:
            self.update_positions()


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
        else:
            self.graphical_edge.set_destination(*source_position)
        self.graphical_edge.update()


    def remove_from_socket(self):
        self.end_socket = None
        self.start_socket = None

    def remove(self):
        self.remove_from_socket()
        self.scene.grscene.removeItem(self.graphical_edge)
        self.graphical_edge = None
        try:
            self.scene.remove_edge(self)
        except ValueError:
            pass

    def serialize(self):
        return OrderedDict([
            ('id', self.id),
            ('edge_type', self.edge_type),
            ('start', self.start_socket.id),
            ('end', self.end_socket.id),
        ])

    def deserialize(self, data, hashmap={}, restore_id = True):
        if restore_id: self.id = data['id']
        self.start_socket = hashmap[data['start']]
        self.end_socket = hashmap[data['end']]
        self.edge_type =  data['edge_type']

