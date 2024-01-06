from MLnode_conf import *
from MLnode_node_base import *
from PyQt5.QtCore import *
from utility import print_traceback
import numpy as np
import torch
import ast

@register_node(OP_NODE_ADD)
class MLNode_Add(MLnode_node):
    icon = "icons/add.png"
    op_code = OP_NODE_ADD
    op_title = "Matrix Addition"
    content_label = "+"
    content_label_objname = "mlnode_node_bg"

    def evalOperation(self, input1, input2):
        return input1 + input2

@register_node(OP_NODE_MATMUL)
class MLNode_Matmul(MLnode_node):
    icon = "icons/matmul.png"
    op_code = OP_NODE_MATMUL
    op_title = "Matrix Multiplication"
    content_label = "X"
    content_label_objname = "mlnode_node_mul"

    def evalOperation(self, input1, input2):
        return np.matmul(input1, input2)

class MLnode_node_transpose_graphicsNode(MLnode_graphicNode):
    def initSizes(self):
        super().initSizes()
        self.width = 150
        self.height = 100

class MLnode_node_transpose_content(QNode_content_widget):
    def initUI(self):
        self.layout = QGridLayout(self)
        self.label_dim0 = QLabel("dim0", self)
        self.edit_dim0 = QLineEdit("0", self)
        self.label_dim1 = QLabel("dim1", self)
        self.edit_dim1 = QLineEdit("1", self)
        self.edit_dim0.setAlignment(Qt.AlignRight)
        self.edit_dim1.setAlignment(Qt.AlignRight)
        self.edit_dim0.setObjectName(self.node.content_label_objname)
        self.edit_dim1.setObjectName(self.node.content_label_objname)
        self.layout.addWidget(self.label_dim0, 0, 0)
        self.layout.addWidget(self.edit_dim0, 0, 1)
        self.layout.addWidget(self.label_dim1, 1, 0)
        self.layout.addWidget(self.edit_dim1, 1, 1)


    def serialize(self):
        res = super().serialize()
        res['dim0'] = self.edit_dim0.text()
        res['dim1'] = self.edit_dim1.text()
        return res
    
    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            dim0 = data['dim0']
            dim1 = data['dim1']
            self.edit_dim0.setText(dim0)
            self.edit_dim1.setText(dim1)
            return True & res
        except Exception as e:print_traceback(e)
        return res
        
@register_node(OP_NODE_TRANSPOSE)
class MLNode_Transpose(MLnode_node):
    icon = "icons/transpose.png"
    op_code = OP_NODE_TRANSPOSE
    op_title = "Transpose"
    content_label = "X"
    content_label_objname = "mlnode_node_transpose"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def initInnerClasses(self):
        self.content = MLnode_node_transpose_content(self)
        self.graphical_node = MLnode_node_transpose_graphicsNode(self)
        self.content.edit_dim0.textChanged.connect(self.onInputChanged)
        self.content.edit_dim1.textChanged.connect(self.onInputChanged)

    
    def evalImplementation(self):
        i1 = self.getInput(0)
        if i1 is None:
            self.markInvalid()
            self.markDescendantsDirty()
            self.graphical_node.setToolTip("Connect all inputs")
            return None
        else:
            u_dim0 = self.content.edit_dim0.text()
            u_dim1 = self.content.edit_dim1.text()
            s_dim0 = int(u_dim0)
            s_dim1 = int(u_dim1)
            val = torch.transpose(i1.eval(), s_dim0, s_dim1)
            self.value = val
            self.markDirty(False)
            self.markInvalid(False)
            self.graphical_node.setToolTip("")
            self.markDescendantsDirty()
            self.evalChildren()
            return val


class MLnode_scalar_graphicsNode(MLnode_graphicNode):
    def initSizes(self):
        super().initSizes()
        self.height = 100.0
        self.title_height = 50.0

class MLnode_scalar_multiply_content(QNode_content_widget):
    def initUI(self):
        self.layout = QHBoxLayout(self)
        self.label = QLabel("Value:", self)
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


@register_node(OP_NODE_SCALAR)
class MLNode_Scalar(MLnode_node):
    icon = "icons/scalar.png"
    op_code = OP_NODE_SCALAR
    op_title = "Scalar Multiplication"
    content_label = "1"
    content_label_objname = "mlnode_node_scalar"
    
    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def initInnerClasses(self):
        self.content = MLnode_scalar_multiply_content(self)
        self.graphical_node = MLnode_scalar_graphicsNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        i1 = self.getInput(0)
        if i1 is None:
            self.markInvalid()
            self.markDescendantsDirty()
            self.graphical_node.setToolTip("Connect all inputs")
            return None
        else:
            # multiply the i1 scalar with the scalar value
            try:
                value_ = self.content.edit.text()
                safe_value_ = float(value_)
                val = i1.eval() * safe_value_
                self.value = val
                self.markDirty(False)
                self.markInvalid(False)
                self.graphical_node.setToolTip(f"{self.value}: {self.get_device_type()}")

                self.markDescendantsDirty()
                self.evalChildren()

                return val
            except Exception as e:
                self.markInvalid()
                self.markDescendantsDirty()
                self.graphical_node.setToolTip("Invalid Scalar")
                return None
            

# node for reshape
class MLnode_reshape_graphicsNode(MLnode_graphicNode):
    def initSizes(self):
        super().initSizes()
        self.width = 150
        self.height = 100

class MLnode_reshape_content(QNode_content_widget):
    def initUI(self):
        self.layout = QHBoxLayout(self)
        self.label = QLabel("Shape:", self)
        self.edit = QLineEdit("1,-1", self)
        self.edit.setAlignment(Qt.AlignRight)
        self.label.setAlignment(Qt.AlignRight)
        self.edit.setObjectName(self.node.content_label_objname)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.edit)
    
    def serialize(self):
        res = super().serialize()
        res['shape'] = self.edit.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            shape = data['shape']
            self.edit.setText(shape)
            return True & res
        except Exception as e:print_traceback(e)
        return res
    
@register_node(OP_NODE_RESHAPE)
class MLnode_reshape(MLnode_node):
    icon = "icons/reshape.png"
    op_code = OP_NODE_RESHAPE
    op_title = "Reshape"
    content_label = "reshape"
    content_label_objname = "mlnode_node_reshape"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def initInnerClasses(self):
        self.content = MLnode_reshape_content(self)
        self.graphical_node = MLnode_reshape_graphicsNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        i1 = self.getInput(0)
        if i1 is None:
            self.markInvalid()
            self.markDescendantsDirty()
            self.graphical_node.setToolTip("Connect all inputs")
            return None
        else:
            # reshape the i1 tensor with the shape value
            try:
                shape_ = self.content.edit.text()
                safe_shape_ = ast.literal_eval(shape_)
                val = i1.eval().reshape(safe_shape_)
                self.value = val
                self.markDirty(False)
                self.markInvalid(False)
                self.graphical_node.setToolTip(f"{self.value}: {self.get_device_type()}")

                self.markDescendantsDirty()
                self.evalChildren()

                return val
            except Exception as e:
                self.markInvalid()
                self.markDescendantsDirty()
                self.graphical_node.setToolTip("Invalid Shape")
                return None