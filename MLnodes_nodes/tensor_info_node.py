from MLnode_conf import *
from MLnode_node_base import *
from PyQt5.QtCore import *
from utility import print_traceback
import numpy as np
import torch

class MLNode_tensor_info_node_graphicNode(MLnode_graphicNode):
    def initSizes(self):
        super().initSizes()
        self.width = 110
        self.height = 110

class MLNode_tensor_info_node_content(QNode_content_widget):
    def initUI(self):
        # have a combo box for the trig function
        self.layout = QVBoxLayout(self)
        self.combo = QComboBox(self)
        self.combo.addItem("shape")
        self.combo.addItem("dtype")
        self.combo.addItem("numelem")
        self.combo.setObjectName(self.node.content_label_objname)
        self.combo.setCurrentIndex(0)
        # change the font size of the combo box
        self.combo.setFont(QFont("Times", 9))
        self.label = QLabel("None", self)
        self.layout.addWidget(self.combo)
        self.layout.addWidget(self.label)

    
    def serialize(self):
        res = super().serialize()
        res["value"] = self.combo.currentText()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.combo.setCurrentText(value)
            return True & res
        except Exception as e:print_traceback(e)
        return res
    
@register_node(OP_NODE_TENSOR_INFO)
class MLNode_tensor_info_node(MLnode_node):
    icon = "icons/tensor_info.png"
    op_code = OP_NODE_TENSOR_INFO
    op_title = "Tensor info"
    content_label = "shape"
    content_label_objname = "mlnode_node_tensor_info"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def initInnerClasses(self):
        self.content = MLNode_tensor_info_node_content(self)
        self.graphical_node = MLNode_tensor_info_node_graphicNode(self)
        self.content.combo.currentIndexChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        i1 = self.getInput(0)
        if i1 is None:
            self.markInvalid()
            self.markDescendantsDirty()
            self.graphical_node.setToolTip("Input is not set")
            return None
        else:
            input_tensor = i1.eval()
            active_info = self.content.combo.currentText()
            if active_info == "shape":
                self.graphical_node.setToolTip(f"shape: {input_tensor.shape}")
                self.content.label.setText(f"shape: \n{input_tensor.shape}")
                val = input_tensor.shape
            elif active_info == "dtype":
                self.graphical_node.setToolTip(f"dtype: {input_tensor.dtype}")
                self.content.label.setText(f"dtype: \n{input_tensor.dtype}")
                val = input_tensor.dtype
            elif active_info == "numelem":
                self.graphical_node.setToolTip(f"number of elements: {input_tensor.numel()}")
                self.content.label.setText(f"numelem: \n{input_tensor.numel()}")
                val = input_tensor.numel()
            else:
                self.markInvalid()
                self.markDescendantsDirty()
                self.graphical_node.setToolTip("Unknown tensor info")
                return None
            
            self.value = val
            self.markDirty(False)
            self.markInvalid(False)
            self.markDescendantsDirty()
            self.evalChildren()
            return self.value