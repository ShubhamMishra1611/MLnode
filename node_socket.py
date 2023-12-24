from node_graphics_socket import Qgraphics_socket
from collections import OrderedDict
from node_serializable import Serializable


LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4

class Socket(Serializable):
    def __init__(self, node, index = 0, position = LEFT_TOP, socket_type = 1, multi_edges = True) -> None:
        super().__init__()
        
        self.node = node
        self.index = index
        self.position = position
        self.socket_type = socket_type
        self.is_multi_edges = multi_edges
        
        self.graphics_socket = Qgraphics_socket(self, self.socket_type)
        self.graphics_socket.setPos(*self.node.get_socket_position(index, position))

        self.edges = []

    def get_socket_position(self):
        return self.node.get_socket_position(self.index, self.position)
        
    
    def add_edge(self, edge):
        self.edges.append(edge)

    # def has_edge(self):
    #     return self.edge is not None
    def remove_edge(self, edge):
        if edge in self.edges: self.edges.remove(edge)
        else: print("!W:", "Socket::removeEdge", "wanna remove edge", edge, "from self.edges but it's not in the list!")

    def removeAllEdges(self):
        while self.edges:
            edge = self.edges.pop(0)
            edge.remove()

    
    def __str__(self) -> str:
        return "<Socket %s %s..%s>" % ("ME" if self.is_multi_edges else "SE", hex(id(self))[2:5], hex(id(self))[-3:])
        return "<Socket %s>" % (hex(id(self)))
    
    
    def serialize(self):
        return OrderedDict([
            ('id', self.id),
            ('index', self.index),
            ('multi_edges', self.is_multi_edges),
            ('position', self.position),
            ('socket_type', self.socket_type),
        ])

    def deserialize(self, data, hashmap={}):
        self.id = data['id']
        self.is_multi_edges = data['multi_edges']
        hashmap[data['id']] = self
        return True




