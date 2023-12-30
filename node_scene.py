import json
from collections import OrderedDict
from node_serializable import Serializable
from node_editor_graphics_scene import Node_Editor_Graphics_Scene
from node_node import Node
from node_edge import Edge
from node_scene_history import scene_history

class InvalidFile(Exception): pass


class scene(Serializable):
    def __init__(self) -> None:
        super().__init__()
        self.nodes = []
        self.edges = []

        self.width, self.height = 16000, 16000
        self._has_been_modified = False
        self._last_selected_items = []
        self._has_been_modified_listeners = []
        self._item_selected_listeners = []
        self._items_deselected_listeners = []




        self.initUI()
        self.history = scene_history(self)
        self.grscene.itemSelected.connect(self.onItemSelected)
        self.grscene.itemsDeselected.connect(self.onItemsDeselected)

    def initUI(self):
        self.grscene = Node_Editor_Graphics_Scene(self)
        self.grscene.set_scene(self.width, self.height)

    def onItemSelected(self):
        current_selected_items = self.getSelectedItems()
        if current_selected_items != self._last_selected_items:
            self._last_selected_items = current_selected_items
            self.history.store_history("Selection Changed")
            for callback in self._item_selected_listeners: callback()


    def onItemsDeselected(self):
        self.resetLastSelectedStates()
        if self._last_selected_items != []:
            self._last_selected_items = []
            self.history.store_history("Deselected Everything")
            for callback in self._items_deselected_listeners: callback()



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

    def addItemSelectedListener(self, callback):
        self._item_selected_listeners.append(callback) 

    def addItemsDeselectedListener(self, callback):
        self._items_deselected_listeners.append(callback)

    def resetLastSelectedStates(self):
        for node in self.nodes:
            node.graphical_node._last_selected_state = False
        for edge in self.edges:
            edge.graphical_edge._last_selected_state = False


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
        print(f'saving to  {filename} was successfull.')

    def loadFromFile(self, filename):
        with open(filename, "r") as file:
            raw_data = file.read().encode('utf-8')
            try:
                data = json.loads(raw_data)
                self.deserialize(data)
            except json.JSONDecodeError:
                raise InvalidFile(f'{file} is not a valid json file')
            except Exception as e:
                print(e)
            

    def getSelectedItems(self):
        return self.grscene.selectedItems()

    
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
    


