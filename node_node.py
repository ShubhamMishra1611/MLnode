import typing
from node_graphics import QgraphicsNode
from node_content_widget import QNode_content_widget
from node_socket import Socket, LEFT_BOTTOM, LEFT_TOP, RIGHT_BOTTOM, RIGHT_TOP
class Node():
    def __init__(self, scene, title="Undefined Node", inputs = [], outputs = []) -> None:
        self.scene = scene
        self.title = title
        self.content = QNode_content_widget()
        self.graphical_node = QgraphicsNode(self)

        self.scene.add_node(self)
        self.scene.grscene.addItem(self.graphical_node)

        self.socket_spacing = 20


        self.inputs = []
        self.outputs = []
        counter = 0

        for item in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_BOTTOM,socket_type = item)
            counter+=1
            self.inputs.append(socket)
        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_TOP,socket_type = item)
            counter+=1
            self.outputs.append(socket)

    @property
    def pos(self):
        return self.graphical_node.pos()
    
    def setPos(self, x, y):
        self.graphical_node.setPos(x, y)
    
    def get_socket_position(self, index, position):
        x = 0 if position in [LEFT_TOP, LEFT_BOTTOM] else self.graphical_node.width
        if position in [LEFT_BOTTOM, RIGHT_BOTTOM]:
            y=self.graphical_node.height - self.graphical_node.edge_size - self.graphical_node._padding - index*self.socket_spacing
        else:
            y = self.graphical_node.title_height + self.graphical_node.edge_size + self.graphical_node._padding + index*self.socket_spacing
        return [x, y]
    
    def update_connected_edges(self):
        for socket in self.inputs + self.outputs:
            if socket.has_edge():
                socket.edge.update_positions()
