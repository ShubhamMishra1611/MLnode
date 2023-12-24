import json
from collections import OrderedDict
from node_serializable import Serializable
from node_editor_graphics_scene import Node_Editor_Graphics_Scene
from node_node import Node
from node_edge import Edge
from node_scene_history import scene_history


class scene(Serializable):
    def __init__(self) -> None:
        super().__init__()
        self.nodes = []
        self.edges = []

        self.width, self.height = 16000, 16000
        self._has_been_modified = False
        self._has_been_modified_listeners = []


        self.initUI()
        self.history = scene_history(self)

    @property
    def has_been_modified(self):
        return False
        return self._has_been_modified

    @has_been_modified.setter
    def has_been_modified(self, value):
        if not self._has_been_modified and value:
            self._has_been_modified = value

            # call all registered listeners
            for callback in self._has_been_modified_listeners:
                callback()

        self._has_been_modified = value


    def addHasBeenModifiedListener(self, callback):
        self._has_been_modified_listeners.append(callback)

    def initUI(self):
        self.grscene = Node_Editor_Graphics_Scene(self)
        self.grscene.set_scene(self.width, self.height)
        

    def add_node(self, node):
        self.nodes.append(node)
    
    def add_edge(self, edge):
        self.edges.append(edge)

    def remove_node(self, node):
        # self.nodes.remove(node)
        if node in self.nodes: self.nodes.remove(node)
        else: print("!W:", "Scene::removeNode", "wanna remove node", node, "from self.nodes but it's not in the list!")


    def remove_edge(self, edge):
        # self.edges.remove(edge)
        if edge in self.edges: self.edges.remove(edge)
        else: print("!W:", "Scene::removeEdge", "wanna remove edge", edge, "from self.edges but it's not in the list!")


    def saveToFile(self, filename):
        with open(filename, "w") as file:
            file.write( json.dumps( self.serialize(), indent=4 ) )
        print("saving to", filename, "was successfull.")

    def loadFromFile(self, filename):
        with open(filename, "r") as file:
            raw_data = file.read().encode('utf-8')
            data = json.loads(raw_data)
            self.deserialize(data)

    def clear(self):
        while len(self.nodes) >0:
            self.nodes[0].remove()
    def serialize(self):
        nodes, edges = [], []
        for node in self.nodes: nodes.append(node.serialize())
        for edge in self.edges: edges.append(edge.serialize())
        return OrderedDict([
            ('id', self.id),
            ('scene_width', self.width),
            ('scene_height', self.height),
            ('nodes', nodes),
            ('edges', edges),
        ])

    def deserialize(self, data, hashmap={}):
        print("deserializating data", data)
        self.clear()

        hashmap = {}

        for node_data in data['nodes']:
            Node(self).deserialize(node_data, hashmap)
        
        for edge_data in data['edges']:
            Edge(self).deserialize(edge_data, hashmap)

        
        return True 
    


