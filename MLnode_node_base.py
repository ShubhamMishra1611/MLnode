from PyQt5.QtWidgets import *
from node_node import Node
from node_content_widget import QNode_content_widget
from node_graphics import QgraphicsNode
from node_socket import LEFT_CENTER, RIGHT_CENTER

class MLnode_graphicNode(QgraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 74
        # self.edge_size = 5
        # self._padding = 8
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

class MLnode_content(QNode_content_widget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)

class MLnode_node(Node):
    icon = ""
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "mlnode_node_bg"

    def __init__(self, scene, inputs=None, outputs=None) -> None:
        if inputs is None:
            inputs = [2,2]
        if outputs is None:
            outputs = [1]

        super().__init__(scene, self.__class__.op_title, inputs, outputs)

    def initInnerClasses(self):
        self.content = MLnode_content(self)
        self.graphical_node = MLnode_graphicNode(self)

    def initSettings(self):
        super().initSettings()
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER


