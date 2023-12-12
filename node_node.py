import typing
from node_graphics import QgraphicsNode
from node_content_widget import QNode_content_widget
class Node():
    def __init__(self, scene, title="Undefined Node") -> None:
        self.scene = scene
        self.title = title
        self.content = QNode_content_widget()
        self.graphical_node = QgraphicsNode(self)

        self.scene.add_node(self)
        self.scene.grscene.addItem(self.graphical_node)


        self.inputs = []
        self.outputs = []
