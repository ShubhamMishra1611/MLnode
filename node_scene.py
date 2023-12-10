from node_editor_graphics_scene import Node_Editor_Graphics_Scene

class scene:
    def __init__(self) -> None:
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
