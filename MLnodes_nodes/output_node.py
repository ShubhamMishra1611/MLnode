from MLnode_conf import *
from MLnode_node_base import *
from PyQt5.QtCore import *
from utility import print_traceback
import numpy as np

class MLnode_output_content(QNode_content_widget):
    def initUI(self):
        self.edit = QLabel("42", self)
        # make it longer 
        self.edit.setMinimumWidth(100)
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

    def evalImplementation(self):
        # self.graphical_node.setToolTip(f'Output Tensor: {self.value.shape}')
        input_node = self.getInput(0)
        if not input_node:
            self.graphical_node.setToolTip('Input is not connected')
            self.markInvalid()
            return
        val = np.array(input_node.eval())
        print(f'val is {val} ')
        if val is None:
            self.graphical_node.setToolTip('Input is NaN')
            self.markInvalid()
            return
            
        output_text = f'{val.shape} {val.dtype}' if val is not None else 'Nothing'
        print(output_text)
        self.content.edit.setText(output_text)
        self.markInvalid(False)
        self.markDirty(False)
        self.graphical_node.setToolTip(f'Output Tensor: {val}')
        return val