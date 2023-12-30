from PyQt5.QtWidgets import *
from node_node import Node
from node_content_widget import QNode_content_widget
from node_graphics import QgraphicsNode

class MLnode_graphicNode(QgraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 74
        self.edge_size = 5
        self._padding = 8

class MLnode_content(QNode_content_widget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)

class MLnode_node(Node):
    def __init__(self, scene, op_code, op_title, content_label="", content_label_objname="calc_node_bg", inputs=None, outputs=None) -> None:
        if inputs is None:
            inputs = [2,2]
        if outputs is None:
            outputs = [1]
        self.op_code = op_code
        self.op_title = op_title
        self.content_label = content_label
        self.content_label_objname = content_label_objname

        super().__init__(scene, self.op_title, inputs, outputs)

    def initInnerClasses(self):
        self.content = MLnode_content(self)
        self.graphical_node = MLnode_graphicNode(self)

