import json
from collections import OrderedDict
from node_serializable import Serializable
from node_editor_graphics_scene import Node_Editor_Graphics_Scene
from node_node import Node
from node_edge import Edge

class scene(Serializable):
    def __init__(self) -> None:
        super().__init__()
        self.nodes = []
        self.edges = []

        self.width, self.height = 16000, 16000

        self.initUI()

    def initUI(self):
        self.grscene = Node_Editor_Graphics_Scene(self)
        self.grscene.set_scene(self.width, self.height)
        

    def add_node(self, node):
        self.nodes.append(node)
    
    def add_edge(self, edge):
        self.edges.append(edge)

    def remove_node(self, node):
        self.nodes.remove(node)

    def remove_edge(self, edge):
        self.edges.remove(edge)

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
    


