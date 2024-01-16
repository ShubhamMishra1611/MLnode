from MLnode_conf import *
from MLnode_node_base import *
from PyQt5.QtCore import *
from utility import print_traceback
import numpy as np
import torch


class MLNode_activations_node_graphicNode(MLnode_graphicNode):
    def initSizes(self):
        super().initSizes()
        self.width = 100
        self.height = 100
        self.title_height = 50.0

class MLNode_activations_node_content(QNode_content_widget):
    def initUI(self):
        self.combo = QComboBox(self)
        self.combo.addItem("relu")
        self.combo.addItem("sigmoid")
        self.combo.addItem("tanh")
        self.combo.addItem("softmax")
        self.combo.setObjectName(self.node.content_label_objname)
        self.combo.setCurrentIndex(0)
        self.combo.setMinimumWidth(90)
        self.combo.setFont(QFont("Times", 12))

    
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
    
@register_node(OP_NODE_ACTIVATION)
class MLNode_activations_node(MLnode_node):
    icon = "icons/relu.png"
    op_code = OP_NODE_ACTIVATION
    op_title = "Activation function"
    content_label = "relu"
    content_label_objname = "mlnode_node_activation"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def initInnerClasses(self):
        self.content = MLNode_activations_node_content(self)
        self.graphical_node = MLNode_activations_node_graphicNode(self)
        self.content.combo.currentIndexChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        i1 = self.getInput(0)
        val = None
        if i1 is None:
            self.markInvalid()
            self.markDescendantsDirty()
            self.graphical_node.setToolTip("Connect all inputs")
            return None
        else:
            active_activation_func = self.content.combo.currentText()
            if active_activation_func == "relu":
                val = torch.nn.ReLU()(i1.eval())
            elif active_activation_func == "sigmoid":
                val = torch.nn.Sigmoid()(i1.eval())
            elif active_activation_func == "tanh":
                val = torch.nn.Tanh()(i1.eval())
            elif active_activation_func == "softmax":
                val = torch.nn.Softmax()(i1.eval())
            else:
                self.markInvalid()
                self.markDescendantsDirty()
                self.graphical_node.setToolTip("Activation function not identified")
                return None
            self.value = val
            self.markDirty(False)
            self.markInvalid(False)
            self.graphical_node.setToolTip("")
            self.markDescendantsDirty()
            self.evalChildren()
            return val
            
