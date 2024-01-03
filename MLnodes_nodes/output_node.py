from MLnode_conf import *
from MLnode_node_base import *
from PyQt5.QtCore import *
from utility import print_traceback

class MLnode_output_content(QNode_content_widget):
    def initUI(self):
        self.edit = QLabel("42", self)
        self.edit.setAlignment(Qt.AlignLeft)
        self.edit.setObjectName(self.node.content_label_objname)

@register_node(OP_NODE_OUTPUT)
class MLNode_Output(MLnode_node):
    icon = "icons/tensoroutput.png"
    op_code = OP_NODE_OUTPUT
    op_title = "Output Tensor"
    content_label_objname = "mlnode_node_output"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[])

    def initInnerClasses(self):
        self.content = MLnode_output_content(self)
        self.graphical_node = MLnode_graphicNode(self)