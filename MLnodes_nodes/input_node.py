from MLnode_conf import *
from MLnode_node_base import *
from PyQt5.QtCore import *
from utility import print_traceback
import numpy as np
import torch
import ast

class MLnode_input_ones_graphicsNode(MLnode_graphicNode):
    def initSizes(self):
        super().initSizes()
        self.width = 150
        self.height = 100
        self.title_height = 50.0


class MLnode_input_ones_content(QNode_content_widget):
    def initUI(self):
        self.layout = QHBoxLayout(self)
        self.label = QLabel("Size:", self)
        self.edit = QLineEdit("1", self)
        self.edit.setAlignment(Qt.AlignRight)
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


@register_node(OP_NODE_INPUT_ONES)
class MLnode_Input(MLnode_node):
    icon = "icons/tensorinput.png"
    op_code = OP_NODE_INPUT_ONES
    op_title = "Input Ones Tensor"
    content_label_objname = "mlnode_node_input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[3])
        self.eval()

    def initInnerClasses(self):
        self.content = MLnode_input_ones_content(self)
        self.graphical_node = MLnode_input_ones_graphicsNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)

    def __is_valid_input(self, input):
        # Check if the input is a list, tuple, torch.Tensor or np.ndarray
        if isinstance(input, (list, tuple, torch.Tensor, np.ndarray)):
            # Convert torch.Tensor or np.ndarray to list
            if isinstance(input, (torch.Tensor, np.ndarray)):
                input = input.tolist()
            # Check if all elements in the input are integers and greater than 0
            if len(input) > 0 and all(isinstance(i, int) and i > 0 for i in input):
                return True
        # Check if the input is a single integer and greater than 0
        elif isinstance(input, int) and input > 0:
            return True
        # If none of the above conditions are met, return False
        return False

    def evalImplementation(self):
        i1 = self.getInput(0)
        try:
            if i1 is not None:
                self.content.edit.setEnabled(False)
                value = i1.eval().shape
                if self.__is_valid_input(value):
                    self.value = torch.ones(value)
            else:
                self.content.edit.setEnabled(True)
                value = self.content.edit.text()
                safe_value = ast.literal_eval(value)
                self.value = torch.ones(safe_value)
        except Exception as e:
            self.markInvalid(True)
            self.markDirty(True)
            self.markDescendantsInvalid(True)
            self.markDescendantsDirty()
            self.graphical_node.setToolTip(f'{e}')
            return None 
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
    
# new node for arange matrix
class MLnode_input_arange_graphicsNode(MLnode_graphicNode):
    def initSizes(self):
        super().initSizes()
        self.width = 150
        self.height = 200

class MLnode_input_arange_content(QNode_content_widget):
    def initUI(self):
        self.layout = QGridLayout(self)
        self.label_start = QLabel("Start:", self)
        self.label_end = QLabel("End:", self)
        self.label_step = QLabel("Step:", self)
        self.edit_start = QLineEdit("1", self)
        self.edit_end = QLineEdit("1", self)
        self.edit_step = QLineEdit("10", self)
        self.edit_start.setAlignment(Qt.AlignRight)
        self.edit_end.setAlignment(Qt.AlignRight)
        self.edit_step.setAlignment(Qt.AlignRight)
        self.label_start.setAlignment(Qt.AlignRight)
        self.label_end.setAlignment(Qt.AlignRight)
        self.label_step.setAlignment(Qt.AlignRight)
        self.edit_start.setObjectName(self.node.content_label_objname)
        self.edit_end.setObjectName(self.node.content_label_objname)
        self.edit_step.setObjectName(self.node.content_label_objname)
        self.layout.addWidget(self.label_start, 0, 0)
        self.layout.addWidget(self.edit_start, 0, 1)
        self.layout.addWidget(self.label_end, 1, 0)
        self.layout.addWidget(self.edit_end, 1, 1)
        self.layout.addWidget(self.label_step, 2, 0)
        self.layout.addWidget(self.edit_step, 2, 1)
    
    def serialize(self):
        res = super().serialize()
        res['value_start'] = self.edit_start.text()
        res['value_end'] = self.edit_end.text()
        res['value_step'] = self.edit_step.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value_start = data['value_start']
            value_end = data['value_end']
            value_step = data['value_step']
            self.edit_start.setText(value_start)
            self.edit_end.setText(value_end)
            self.edit_step.setText(value_step)
            return True & res
        except Exception as e:print_traceback(e)
        return res
    

@register_node(OP_NODE_INPUT_ARANGE)
class MLnode_Input_arange(MLnode_node):
    icon = "icons/tensorinput.png"
    op_code = OP_NODE_INPUT_ARANGE
    op_title = "Input Arange"
    content_label_objname = "mlnode_node_input_arange"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])
        self.eval()

    def initInnerClasses(self):
        self.content = MLnode_input_arange_content(self)
        self.graphical_node = MLnode_input_arange_graphicsNode(self)
        self.content.edit_start.textChanged.connect(self.onInputChanged)
        self.content.edit_end.textChanged.connect(self.onInputChanged)
        self.content.edit_step.textChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        unsafe_start_value = self.content.edit_start.text()
        unsafe_end_value = self.content.edit_end.text()
        unsafe_step_value = self.content.edit_step.text()
        safe_start_value = float(unsafe_start_value) if unsafe_start_value else 0.0
        safe_end_value = float(unsafe_end_value) if unsafe_end_value else 10.0
        safe_step_value = float(unsafe_step_value) if unsafe_step_value else 1.0
        try:
            self.value = torch.arange(safe_start_value, safe_end_value, safe_step_value)
            self.markDirty(False)
            self.markInvalid(False)

            self.markDescendantsInvalid(False)
            self.markDescendantsDirty()

            self.graphical_node.setToolTip(f'Input Arange Tensor: Shape = {self.value.shape}, dtype = {self.value.dtype}')
            self.evalChildren()
            return self.value
        except Exception as e:
            print_traceback(e)
            self.markInvalid(True)
            self.markDirty(True)
            self.markDescendantsInvalid(True)
            self.markDescendantsDirty()
            self.graphical_node.setToolTip(f'{e}')
            return None




