from MLnode_conf import *
from MLnode_node_base import *
from PyQt5.QtCore import *
from utility import print_traceback
import numpy as np

class MLnode_input_content(QNode_content_widget):
    def initUI(self):
        self.edit = QLineEdit("1", self)
        self.edit.setAlignment(Qt.AlignRight)
        self.edit.setObjectName(self.node.content_label_objname)
    
    def serialize(self):
        res = super().serialize()
        res['value'] = self.edit.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.edit.setText(value)
            return True & res
        except Exception as e:print_traceback(e)
        return res


@register_node(OP_NODE_INPUT)
class MLnode_Input(MLnode_node):
    icon = "icons/tensorinput.png"
    op_code = OP_NODE_INPUT
    op_title = "Input Tensor"
    content_label_objname = "mlnode_node_input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])
        self.eval()

    def initInnerClasses(self):
        self.content = MLnode_input_content(self)
        self.graphical_node = MLnode_graphicNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        unsafe_value = self.content.edit.text()
        safe_value = int(unsafe_value)
        self.value = np.ones(shape=(safe_value,safe_value+1))
        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.graphical_node.setToolTip(f'Input Tensor: Shape = {self.value.shape}, dtype = {self.value.dtype}')

        self.evalChildren()

        return self.value
    
# new node for eye matrix

class MLnode_input_eye_content(QNode_content_widget):
    def initUI(self):
        self.layout = QHBoxLayout(self)
        self.label = QLabel("Size:", self)
        self.edit = QLineEdit("1", self)
        self.edit.setAlignment(Qt.AlignRight)
        self.label.setAlignment(Qt.AlignRight)
        self.edit.setObjectName(self.node.content_label_objname)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.edit)
    
    def serialize(self):
        res = super().serialize()
        res['value'] = self.edit.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.edit.setText(value)
            return True & res
        except Exception as e:print_traceback(e)
        return res
    

@register_node(OP_NODE_INPUT_EYE)
class MLnode_Input_eye(MLnode_node):
    icon = "icons/tensorinput.png"
    op_code = OP_NODE_INPUT_EYE
    op_title = "Input Eye Tensor"
    content_label_objname = "mlnode_node_input_eye"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])
        self.eval()

    def initInnerClasses(self):
        self.content = MLnode_input_eye_content(self)
        self.graphical_node = MLnode_graphicNode(self)
        print(f'My content layout is {self.content.layout}')
        self.content.edit.textChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        unsafe_value = self.content.edit.text()
        safe_value = int(unsafe_value)
        self.value = np.eye(safe_value)
        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.graphical_node.setToolTip(f'Input Eye Tensor: Shape = {self.value.shape}, dtype = {self.value.dtype}')

        self.evalChildren()

        return self.value


