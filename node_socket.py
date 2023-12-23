from node_graphics_socket import Qgraphics_socket
from collections import OrderedDict
from node_serializable import Serializable


LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4

class Socket(Serializable):
    def __init__(self, node, index = 0, position = LEFT_TOP, socket_type = 1) -> None:
        super().__init__()
        
        self.node = node
        self.index = index
        self.position = position
        self.socket_type = socket_type
        
        self.graphics_socket = Qgraphics_socket(self, self.socket_type)
        self.graphics_socket.setPos(*self.node.get_socket_position(index, position))

        self.edge = None

    def get_socket_position(self):
        return self.node.get_socket_position(self.index, self.position)
        
    
    def set_connected_edge(self, edge=None):
        self.edge = edge

    def has_edge(self):
        return self.edge is not None
    
    def __str__(self) -> str:
        return "<Socket %s>" % (hex(id(self)))
    
    def serialize(self):
        return OrderedDict([
            ('id', self.id),
            ('index', self.index),
            ('position', self.position),
            ('socket_type', self.socket_type),
        ])

    def deserialize(self, data, hashmap={}):
        self.id = data['id']
        hashmap[data['id']] = self
        return True




