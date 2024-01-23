from node_graphics_socket import Qgraphics_socket
from collections import OrderedDict
from node_serializable import Serializable


LEFT_TOP = 1
LEFT_CENTER =2
LEFT_BOTTOM = 3
RIGHT_TOP = 4
RIGHT_CENTER = 5
RIGHT_BOTTOM = 6


class Socket(Serializable):
    def __init__(self, node, index = 0, position = LEFT_TOP, socket_type = 1, multi_edges = True, count_on_this_node_side=1, is_input=False) -> None:
        super().__init__()
        
        self.node = node
        self.index = index
        self.position = position
        self.socket_type = socket_type
        self.is_multi_edges = multi_edges
        self.count_on_this_node_side = count_on_this_node_side
        self.is_input = is_input
        self.is_output = not self.is_input

        
        self.graphics_socket = Qgraphics_socket(self, self.socket_type)
        self.setSocketPosition()

        self.edges = []

    def get_socket_position(self):
        res = self.node.get_socket_position(self.index, self.position, self.count_on_this_node_side)
        return res
    
    def setSocketPosition(self):
        self.graphics_socket.setPos(*self.node.get_socket_position(self.index, self.position, self.count_on_this_node_side))

        
    
    def add_edge(self, edge):
        self.edges.append(edge)

    def remove_edge(self, edge):
        if edge in self.edges: self.edges.remove(edge)
        else: print("!W:", "Socket::removeEdge", "wanna remove edge", edge, "from self.edges but it's not in the list!")

    def removeAllEdges(self):
        while self.edges:
            edge = self.edges.pop(0)
            edge.remove()

    
    def __str__(self) -> str:
        return "<Socket %s %s..%s>" % ("ME" if self.is_multi_edges else "SE", hex(id(self))[2:5], hex(id(self))[-3:])
    
    
    def serialize(self):
        return OrderedDict([
            ('id', self.id),
            ('index', self.index),
            ('multi_edges', self.is_multi_edges),
            ('position', self.position),
            ('socket_type', self.socket_type),
        ])

    def deserialize(self, data, hashmap={}, restore_id = True):
        if restore_id:self.id = data['id']
        self.is_multi_edges = data['multi_edges']
        hashmap[data['id']] = self
        return True




