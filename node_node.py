import typing
from collections import OrderedDict
from node_serializable import Serializable
from node_graphics import QgraphicsNode
from node_content_widget import QNode_content_widget
from node_socket import Socket, LEFT_BOTTOM, LEFT_TOP, RIGHT_BOTTOM, RIGHT_TOP, LEFT_CENTER, RIGHT_CENTER
DEBUG = False
class Node(Serializable):
    def __init__(self, scene, title="Undefined Node", inputs = [], outputs = []) -> None:
        super().__init__()
        self._title = title
        self.scene = scene
        # self.content = QNode_content_widget(self)
        # self.graphical_node = QgraphicsNode(self)
        self.initInnerClasses()
        self.initSettings()


        self.title = title
        self.scene.add_node(self)
        self.scene.grscene.addItem(self.graphical_node)
        # self.socket_spacing = 20


        self.inputs = []
        self.outputs = []
        self.initSockets(inputs, outputs)

    def __str__(self) -> str:
        return "<Node %s>" % (hex(id(self)))
    
    def initInnerClasses(self):
        self.content = QNode_content_widget(self)
        self.graphical_node = QgraphicsNode(self)

    def initSettings(self):
        self.socket_spacing = 20

        self.input_socket_position = LEFT_BOTTOM
        self.output_socket_position = RIGHT_TOP
        self.input_multi_edged = False
        self.output_multi_edged = True

    def initSockets(self, inputs, outputs, reset=True):
        """ Create sockets for inputs and outputs"""

        if reset:
            # clear old sockets
            if hasattr(self, 'inputs') and hasattr(self, 'outputs'):
                # remove grSockets from scene
                for socket in (self.inputs+self.outputs):
                    self.scene.grscene.removeItem(socket.graphics_socket)
                self.inputs = []
                self.outputs = []

        counter = 0

        for item in inputs:
            socket = Socket(node=self, index=counter, position=self.input_socket_position,
                            socket_type = item, multi_edges=self.input_multi_edged, 
                            count_on_this_node_side=len(inputs), is_input=True)
            counter+=1
            self.inputs.append(socket)
        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=self.output_socket_position,
                            socket_type = item, multi_edges=self.output_multi_edged, 
                            count_on_this_node_side=len(outputs), is_input=False)
            counter+=1
            self.outputs.append(socket)



    

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
    
    
    def get_socket_position(self, index, position, num_out_of=1):
        x = 0 if position in [LEFT_TOP,LEFT_CENTER,  LEFT_BOTTOM] else self.graphical_node.width
        if position in [LEFT_BOTTOM, RIGHT_BOTTOM]:
            y=self.graphical_node.height - self.graphical_node.edge_roundness - self.graphical_node.title_vertical_padding - index*self.socket_spacing
        elif position in (LEFT_CENTER, RIGHT_CENTER):
            num_sockets = num_out_of
            node_height = self.graphical_node.height
            top_offset = self.graphical_node.title_height + 2 * self.graphical_node.title_vertical_padding + self.graphical_node.edge_padding
            available_height = node_height - top_offset

            total_height_of_all_sockets = num_sockets * self.socket_spacing
            new_top = available_height - total_height_of_all_sockets

            y = top_offset + available_height/2.0 + (index-0.5)*self.socket_spacing
            if num_sockets > 1:
                y -= self.socket_spacing * (num_sockets-1)/2

        elif position in (LEFT_TOP, RIGHT_TOP):
            y = self.graphical_node.title_height + self.graphical_node.title_vertical_padding + index*self.socket_spacing
        else:
            y = 0
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
        num_inputs = len( data['inputs'] )
        num_outputs = len( data['outputs'] )


        self.inputs = []
        print(data['inputs'])
        for socket_data in data['inputs']:
            new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'],
                                socket_type=socket_data['socket_type'], count_on_this_node_side=num_inputs, is_input=True)
            new_socket.deserialize(socket_data, hashmap)
            self.inputs.append(new_socket)
        self.outputs = []
        for socket_data in data['outputs']:
            new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'],
                                socket_type=socket_data['socket_type'], count_on_this_node_side=num_outputs, is_input=False)
            new_socket.deserialize(socket_data, hashmap)
            self.outputs.append(new_socket)
        
        return True

