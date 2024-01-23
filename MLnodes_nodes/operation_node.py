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

    
    def evalImplementation(self, index = 0):
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
            self.value[index] = val
            self.markDirty(False)
            self.markInvalid(False)
            self.graphical_node.setToolTip("")
            self.markDescendantsDirty()
            self.evalChildren()
            return self.value


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

    def evalImplementation(self, index = 0):
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
                self.value[index] = val
                self.markDirty(False)
                self.markInvalid(False)
                self.graphical_node.setToolTip(f"{self.value[index]}: {self.get_device_type()}")

                self.markDescendantsDirty()
                self.evalChildren()

                return self.value
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

    def evalImplementation(self, index = 0):
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
                self.value[index] = val
                self.markDirty(False)
                self.markInvalid(False)
                self.graphical_node.setToolTip(f"{self.value[index]}: {self.get_device_type()}")

                self.markDescendantsDirty()
                self.evalChildren()

                return self.value
            except Exception as e:
                self.markInvalid()
                self.markDescendantsDirty()
                self.graphical_node.setToolTip("Invalid Shape")
                return None
            
class MLnode_flatten_graphicsNode(MLnode_graphicNode):
    def initSizes(self):
        super().initSizes()
        self.width = 150
        self.height = 100

class MLnode_flatten_content(QNode_content_widget):
    def initUI(self):
        self.layout = QGridLayout(self)
        self.label_dim0 = QLabel("dim0", self)
        self.edit_dim0 = QLineEdit("0", self)
        self.label_dim1 = QLabel("dim1", self)
        self.edit_dim1 = QLineEdit("-1", self)
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
    
@register_node(OP_NODE_FLATTEN)
class MLnode_flatten(MLnode_node):
    icon = "icons/flatten.png"
    op_code = OP_NODE_FLATTEN
    op_title = "Flatten"
    content_label = "flatten"
    content_label_objname = "mlnode_node_flatten"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def initInnerClasses(self):
        self.content = MLnode_flatten_content(self)
        self.graphical_node = MLnode_flatten_graphicsNode(self)
        self.content.edit_dim0.textChanged.connect(self.onInputChanged)
        self.content.edit_dim1.textChanged.connect(self.onInputChanged)

    
    def evalImplementation(self, index = 0):
        i1 = self.getInput(0)
        if i1 is None:
            self.markInvalid()
            self.markDescendantsDirty()
            self.graphical_node.setToolTip("Connect all inputs")
            return None
        else:
            try:
                u_dim0 = self.content.edit_dim0.text()
                u_dim1 = self.content.edit_dim1.text()
                s_dim0 = int(u_dim0)
                s_dim1 = int(u_dim1)
                val = torch.flatten(i1.eval(), s_dim0, s_dim1)
                self.value[index] = val
                self.markDirty(False)
                self.markInvalid(False)
                self.graphical_node.setToolTip("")
                self.markDescendantsDirty()
                self.evalChildren()
                return self.value
            except Exception as e:
                self.markInvalid()
                self.markDescendantsDirty()
                self.graphical_node.setToolTip("Invalid Shape")
                return None
            
class MLnode_normalization_graphicsNode(MLnode_graphicNode):
    def initSizes(self):
        super().initSizes()
        self.width = 150
        self.height = 80

class MLnode_normalization_content(QNode_content_widget):
    def initUI(self):
        self.layout = QHBoxLayout(self)
        self.label = QLabel("Normalize", self)
        self.layout.addWidget(self.label)

    def serialize(self):
        res = super().serialize()
        return res
    
    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            return True & res
        except Exception as e:print_traceback(e)
        return res
    
@register_node(OP_NODE_NORMALIZATION)
class MLnode_normalization(MLnode_node):
    icon = "icons/normalization.png"
    op_code = OP_NODE_NORMALIZATION
    op_title = "Normalization"
    content_label = "normalization"
    content_label_objname = "mlnode_node_normalization"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def initInnerClasses(self):
        self.content = MLnode_normalization_content(self)
        self.graphical_node = MLnode_normalization_graphicsNode(self)

    
    def evalImplementation(self, index = 0):
        i1 = self.getInput(0)
        if i1 is None:
            self.markInvalid()
            self.markDescendantsDirty()
            self.graphical_node.setToolTip("Connect all inputs")
            return None
        else:
            try:
                this_tensor = i1.eval()
                # ensure that tensor is not 1D
                if len(this_tensor.shape) == 1:
                    this_tensor = this_tensor.unsqueeze(0)
                val = torch.nn.functional.normalize(this_tensor)
                self.value[index] = val
                self.markDirty(False)
                self.markInvalid(False)
                self.graphical_node.setToolTip("")
                self.markDescendantsDirty()
                self.evalChildren()
                return self.value
            except Exception as e:
                self.markInvalid()
                self.markDescendantsDirty()
                self.graphical_node.setToolTip(f"{e}")
                return None
            

class MLnode_clipping_graphicsNode(MLnode_graphicNode):
    def initSizes(self):
        super().initSizes()
        self.width = 150
        self.height = 100

class MLnode_clipping_content(QNode_content_widget):
    def initUI(self):
        self.layout = QGridLayout(self)
        self.label_min = QLabel("min", self)
        self.edit_min = QLineEdit("0.0", self)
        self.label_max = QLabel("max", self)
        self.edit_max = QLineEdit("1.0", self)
        self.edit_min.setObjectName(self.node.content_label_objname)
        self.edit_max.setObjectName(self.node.content_label_objname)
        self.layout.addWidget(self.label_min, 0, 0)
        self.layout.addWidget(self.edit_min, 0, 1)
        self.layout.addWidget(self.label_max, 1, 0)
        self.layout.addWidget(self.edit_max, 1, 1)

    def serialize(self):
        res = super().serialize()
        res['min'] = self.edit_min.text()
        res['max'] = self.edit_max.text()
        return res
    
    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            min = data['min']
            max = data['max']
            self.edit_min.setText(min)
            self.edit_max.setText(max)
            return True & res
        except Exception as e:print_traceback(e)
        return res
    

@register_node(OP_NODE_CLIPPING)
class MLnode_clipping(MLnode_node):
    icon = "icons/clipping.png"
    op_code = OP_NODE_CLIPPING
    op_title = "Clipping"
    content_label = "clipping"
    content_label_objname = "mlnode_node_clipping"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def initInnerClasses(self):
        self.content = MLnode_clipping_content(self)
        self.graphical_node = MLnode_clipping_graphicsNode(self)
        self.content.edit_min.textChanged.connect(self.onInputChanged)
        self.content.edit_max.textChanged.connect(self.onInputChanged)

    
    def evalImplementation(self, index = 0):
        i1 = self.getInput(0)
        if i1 is None:
            self.markInvalid()
            self.markDescendantsDirty()
            self.graphical_node.setToolTip("Connect all inputs")
            return None
        else:
            try:
                u_min = self.content.edit_min.text()
                u_max = self.content.edit_max.text()
                s_min = float(u_min)
                s_max = float(u_max)
                val = torch.clamp(i1.eval(), s_min, s_max)
                self.value[index] = val
                self.markDirty(False)
                self.markInvalid(False)
                self.graphical_node.setToolTip("")
                self.markDescendantsDirty()
                self.evalChildren()
                return self.value
            except Exception as e:
                self.markInvalid()
                self.markDescendantsDirty()
                self.graphical_node.setToolTip(f"{e}")
                return None
            
class MLnode_changedtype_graphicsNode(MLnode_graphicNode):
    def initSizes(self):
        super().initSizes()
        self.width = 150
        self.height = 100

class MLnode_changedtype_content(QNode_content_widget):
    def initUI(self):
        self.layout = QGridLayout(self)
        self.label_type = QLabel("type", self)
        self.combo_type = QComboBox(self)
        types = ["float32", "float64", "int32", "int64", "uint8", "bool"]

        for type in types:
            self.combo_type.addItem(type)
        self.combo_type.setObjectName(self.node.content_label_objname)

        self.layout.addWidget(self.label_type, 0, 0)
        self.layout.addWidget(self.combo_type, 0, 1)

    def serialize(self):
        res = super().serialize()
        res['type'] = self.combo_type.currentText()
        return res
    
    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            type = data['type']
            self.combo_type.setCurrentText(type)
            return True & res
        except Exception as e:print_traceback(e)
        return res
    

@register_node(OP_NODE_CHANGEDTYPE)
class MLnode_changedtype(MLnode_node):
    icon = "icons/changedtype.png"
    op_code = OP_NODE_CHANGEDTYPE
    op_title = "Changed Type"
    content_label = "changedtype"
    content_label_objname = "mlnode_node_changedtype"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def initInnerClasses(self):
        self.content = MLnode_changedtype_content(self)
        self.graphical_node = MLnode_changedtype_graphicsNode(self)
        self.content.combo_type.currentTextChanged.connect(self.onInputChanged)

    
    def evalImplementation(self, index = 0):
        i1 = self.getInput(0)
        if i1 is None:
            self.markInvalid()
            self.markDescendantsDirty()
            self.graphical_node.setToolTip("Connect all inputs")
            return None
        else:
            try:
                u_type = self.content.combo_type.currentText()
                dtype_map = {
                    "float32": torch.float32,
                    "float64": torch.float64,
                    "int32": torch.int32,
                    "int64": torch.int64,
                    "uint8": torch.uint8,
                    "bool": torch.bool
                }
                val = i1.eval().type(dtype_map[u_type])
                self.value[index] = val
                self.markDirty(False)
                self.markInvalid(False)
                self.graphical_node.setToolTip("")
                self.markDescendantsDirty()
                self.evalChildren()
                return self.value
            except Exception as e:
                self.markInvalid()
                self.markDescendantsDirty()
                self.graphical_node.setToolTip(f"{e}")
                return None