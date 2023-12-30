import typing
from collections import OrderedDict
from node_serializable import Serializable
from node_graphics import QgraphicsNode
from node_content_widget import QNode_content_widget
from node_socket import Socket, LEFT_BOTTOM, LEFT_TOP, RIGHT_BOTTOM, RIGHT_TOP
DEBUG = False
class Node(Serializable):
    def __init__(self, scene, title="Undefined Node", inputs = [], outputs = []) -> None:
        super().__init__()
        self._title = title
        self.scene = scene
        self.content = QNode_content_widget(self)
        self.graphical_node = QgraphicsNode(self)

        self.title = title
        self.scene.add_node(self)
        self.scene.grscene.addItem(self.graphical_node)
        self.socket_spacing = 20


        self.inputs = []
        self.outputs = []
        counter = 0

        for item in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_BOTTOM,socket_type = item, multi_edges=False)
            counter+=1
            self.inputs.append(socket)
        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_TOP,socket_type = item, multi_edges=True)
            counter+=1
            self.outputs.append(socket)

    def __str__(self) -> str:
        return "<Node %s>" % (hex(id(self)))
    

    @property
    def pos(self):
        return self.graphical_node.pos()
    def setPos(self, x, y):
        self.graphical_node.setPos(x, y)
    @property
    def title(self): return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.graphical_node.title = self._title
    
    
    def get_socket_position(self, index, position):
        x = 0 if position in [LEFT_TOP, LEFT_BOTTOM] else self.graphical_node.width
        if position in [LEFT_BOTTOM, RIGHT_BOTTOM]:
            y=self.graphical_node.height - self.graphical_node.edge_size - self.graphical_node._padding - index*self.socket_spacing
        else:
            y = self.graphical_node.title_height + self.graphical_node.edge_size + self.graphical_node._padding + index*self.socket_spacing
        return [x, y]
    
    def update_connected_edges(self):
        for socket in self.inputs + self.outputs:
            # if socket.has_edge():
            #     socket.edge.update_positions()
            for edge in socket.edges:
                edge.update_positions()


    def remove(self):
        if DEBUG: print('> Removing node ', self)
        if DEBUG: print('removing all edges from the socket')
        for socket in (self.inputs + self.outputs):
            # if socket.has_edge():
            #     if DEBUG: print(' ---- removing socket:', socket, 'edge ', socket.edge)
            #     socket.edge.remove()
            for edge in socket.edges:
                if DEBUG: print("    - removing from socket:", socket, "edge:", edge)
                edge.remove()
        if DEBUG: print('removing grNode')
        self.scene.grscene.removeItem(self.graphical_node)
        self.graphical_node = None
        if DEBUG: print('remove node from the scene')
        self.scene.remove_node(self)
            
        if DEBUG: print('- everything was done')

    def serialize(self):
        inputs, outputs = [], []
        for socket in self.inputs: inputs.append(socket.serialize())
        for socket in self.outputs: outputs.append(socket.serialize())
        return OrderedDict([
            ('id', self.id),
            ('title', self.title),
            ('pos_x', self.graphical_node.scenePos().x()),
            ('pos_y', self.graphical_node.scenePos().y()),
            ('inputs', inputs),
            ('outputs', outputs),
            ('content', self.content.serialize()),
        ])

    def deserialize(self, data, hashmap={}):
        self.id = data['id']
        hashmap[data['id']] = self
        self.setPos(data['pos_x'], data['pos_y'])
        self.title = data['title']

        data['inputs'].sort(key = lambda socket: socket['index']+socket['position']*10000)
        data['outputs'].sort(key = lambda socket: socket['index']+socket['position']*10000)

        self.inputs = []
        print(data['inputs'])
        for socket_data in data['inputs']:
            new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'],
                                socket_type=socket_data['socket_type'])
            new_socket.deserialize(socket_data, hashmap)
            self.inputs.append(new_socket)
        self.outputs = []
        for socket_data in data['outputs']:
            new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'],
                                socket_type=socket_data['socket_type'])
            new_socket.deserialize(socket_data, hashmap)
            self.outputs.append(new_socket)
        
        return True

