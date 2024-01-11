from MLnode_conf import *
from MLnode_node_base import *
from PyQt5.QtCore import *
from utility import print_traceback
import numpy as np
import torch

class MLNode_nnLinear_graphicsNode(MLnode_graphicNode):
    def initSizes(self):
        super().initSizes()
        self.width = 150
        self.height = 100

class MLNode_nnLinear_content(QNode_content_widget):
    def initUI(self):
        self.layout = QGridLayout(self)
        self.label_inchannel = QLabel("In-channel", self)
        self.label_outchannel = QLabel("Out-channel", self)

        self.edit_inchannel = QLineEdit('64', self)
        self.edit_outchannel = QLineEdit('32', self)
        self.edit_inchannel.setMinimumWidth(50)
        self.edit_outchannel.setMinimumWidth(50)

        self.edit_inchannel.setObjectName(self.node.content_label_objname)
        self.edit_outchannel.setObjectName(self.node.content_label_objname)

        self.layout.addWidget(self.label_inchannel, 0, 0)
        self.layout.addWidget(self.label_outchannel, 1, 0)

        self.layout.addWidget(self.edit_inchannel, 0, 1)
        self.layout.addWidget(self.edit_outchannel, 1, 1)

    def serialize(self):
        res = super().serialize()
        res['value_inchannel'] = self.edit_inchannel.text()
        res['value_outchannel'] = self.edit_outchannel.text()
        return res
    
    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value_inchannel = data['value_inchannel']
            value_outchannel = data['value_outchannel']
            self.edit_inchannel.setText(value_inchannel)
            self.edit_outchannel.setText(value_outchannel)
            return True & res
        except Exception as e:print_traceback(e)
        return res
    
@register_node(OP_NODE_NN_LINEAR)
class MLNode_nnLinear(MLnode_node):
    icon = "icons/nnLinear.png"
    op_code = OP_NODE_NN_LINEAR
    op_title = "nn.Linear"
    content_label = "nn.Linear"
    content_label_objname = "mlnode_node_nnLinear"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def initInnerClasses(self):
        self.content = MLNode_nnLinear_content(self)
        self.graphical_node = MLNode_nnLinear_graphicsNode(self)
        self.content.edit_inchannel.textChanged.connect(self.onInputChanged)
        self.content.edit_outchannel.textChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        u_inchannel = self.content.edit_inchannel.text()
        u_outchannel = self.content.edit_outchannel.text()

        input_node = self.getInput(0)
        if input_node is None:
            self.markInvalid()
            self.markDescendantsDirty()
            self.graphical_node.setToolTip("Connect all inputs")
            return None
        try:
            input_tensor = input_node.eval()
            if input_tensor.shape[0] != int(u_inchannel): # check if input_value can be given to nn.Linear
                self.markInvalid()
                self.markDescendantsDirty()
                self.graphical_node.setToolTip("Input shape does not match with the input channel")
                return None
            inchannel = int(u_inchannel)
            outchannel = int(u_outchannel)
            val = torch.nn.Linear(inchannel, outchannel, bias=True)(input_node.eval())
            self.value = val
            self.markDirty(False)
            self.markInvalid(False)
            self.graphical_node.setToolTip("")
            self.evalChildren()
            return val
        except Exception as e:
            self.markInvalid()
            self.markDescendantsDirty()
            self.graphical_node.setToolTip("Invalid input")
            return None
        
    def getImplemClassInstance(self):
        hex_val = hex(id(self))[2:]
        
        for node in self.getChildrenNodes():
            node.getImplemClassInstance()

        for node in self.getParentNodes():
            node.getImplemClassInstance()
        
        if not self.isDirty() and not self.isInvalid():
            return [torch.nn.Linear(self.inchannel,
                                   self.outchannel), hex_val]
        else:
            return None

