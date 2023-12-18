from node_graphics_socket import Qgraphics_socket

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4

class Socket():
    def __init__(self, node, index = 0, position = LEFT_TOP) -> None:
        
        self.node = node
        self.index = index
        self.position = position
        
        self.graphics_socket = Qgraphics_socket(self.node.graphical_node)
        self.graphics_socket.setPos(*self.node.get_socket_position(index, position))

