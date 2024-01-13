from MLnode_conf import *
from MLnode_node_base import *
from PyQt5.QtCore import *
from utility import print_traceback
import numpy as np
import torch 

class MLnode_output_content(QNode_content_widget):
    def initUI(self):
        self.edit = QLabel("None", self)
        # make it longer 
        self.edit.setMinimumWidth(180)
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
        input_node = self.getInput(0)
        if not input_node:
            self.graphical_node.setToolTip('Input is not connected')
            self.markInvalid()
            return
        try:
            val = torch.tensor(input_node.eval())
        except Exception as e:
            self.graphical_node.setToolTip(f'Could not convert input to numpy array: {e}')
            self.markInvalid()
            return
        if val is None:
            self.graphical_node.setToolTip('Input is NaN')
            self.markInvalid()
            return
            
        output_text = f'shape:{val.shape} dtype:{val.dtype}' 
        print(output_text)
        self.content.edit.setText(output_text)
        self.markInvalid(False)
        self.markDirty(False)
        self.graphical_node.setToolTip(f'Output Tensor: shape: {val.shape}\n dtype: {val.dtype}\n{val}')
        return val