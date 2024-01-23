from MLnode_conf import *
from MLnode_node_base import *
from PyQt5.QtCore import *
from utility import print_traceback
import numpy as np
import torch
from torchvision.io import read_image
import pandas as pd
import glob
import os
from MLnode_object import MLnode_obj

class MLnode_getdata_graphicsNode(MLnode_graphicNode):
    def initSizes(self):
        super().initSizes()
        self.width = 150
        self.height = 160

class MLnode_getdata_content(QNode_content_widget):
    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.label_file_name = QLabel("File location (csv)")

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse)
        self.y_col_label = QLabel("Y column")
        self.y_col = QLineEdit()
        self.y_col.setText("-1")
        self.browse_button.setObjectName(self.node.content_label_objname)
        self.y_col.setObjectName(self.node.content_label_objname)

        self.file = None
        self.file_path = None

        self.layout.addWidget(self.label_file_name)
        self.layout.addWidget(self.browse_button)
        self.layout.addWidget(self.y_col_label)
        self.layout.addWidget(self.y_col)

    def browse(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file')[0]
        self.file_path = file_name
        file_name = os.path.basename(file_name)
        self.label_file_name.setText(file_name)
        self.file = file_name

    def serialize(self):
        res = super().serialize()
        res['value_file_name'] = self.file_path
        res['y_col'] = self.y_col.text()
        return res
    
    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value_file_name = data['value_file_name']
            y_col = data['y_col']
            self.label_file_name.setText(os.path.basename(value_file_name))
            self.y_col.setText(y_col)
            return True & res
        except Exception as e:print_traceback(e)
        return res
    

@register_node(OP_NODE_GETDATA)
class MLnode_getdata(MLnode_node):
    icon = "icons/getdata.png"
    op_code = OP_NODE_GETDATA
    op_title = "getdata"
    content_label = "getdata"
    content_label_objname = "mlnode_node_getdata"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[1])

    def initInnerClasses(self):
        self.content = MLnode_getdata_content(self)
        self.graphical_node = MLnode_getdata_graphicsNode(self)
    
    def evalImplementation(self, index = 0):
        try:
            if self.content.file is None:
                return None
            else:
                # check if file is csv
                if self.content.file_path.endswith('csv'):
                    data = pd.read_csv(self.content.file_path)
                    data = data.to_numpy(dtype=np.float32)
                    data = torch.from_numpy(data)
                    print(f"Data shape: {data.shape}")
                    y_col = int(self.content.y_col.text())
                    if y_col == -1:
                        y_col = data.shape[1]-1
                    data = data[:, :y_col]
                    print(f"Y shape: {data.shape}")
                    self.markInvalid(False)
                    self.markDirty(False)
                    self.graphical_node.setToolTip(f"Shape: {data.shape}")
                    self.value = data[0]
                    return self.value
                else:
                    self.markInvalid()
                    self.graphical_node.setToolTip("File type not supported")
                    return None        
        except Exception as e:print_traceback(e)

class MLnode_getimgdata_content(QNode_content_widget):
    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.label_file_name = QLabel("File location (png)")

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse)
        self.browse_button.setObjectName(self.node.content_label_objname)

        self.file = None
        self.file_path = None

        self.layout.addWidget(self.label_file_name)
        self.layout.addWidget(self.browse_button)

    def browse(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file')[0]
        self.file_path = file_name
        file_name = os.path.basename(file_name)
        self.label_file_name.setText(file_name)
        self.file = file_name

    def serialize(self):
        res = super().serialize()
        res['value_file_name'] = self.file_path
        return res
    
    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value_file_name = data['value_file_name']
            self.label_file_name.setText(os.path.basename(value_file_name))
            return True & res
        except Exception as e:print_traceback(e)
        return res
    

@register_node(OP_NODE_GETIMGDATA)
class MLnode_getimgdata(MLnode_node):
    icon = "icons/getdata.png"
    op_code = OP_NODE_GETIMGDATA
    op_title = "getimgdata"
    content_label = "getimgdata"
    content_label_objname = "mlnode_node_getimgdata"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[1])

    def initInnerClasses(self):
        self.content = MLnode_getimgdata_content(self)
        self.graphical_node = MLnode_getdata_graphicsNode(self)
    
    def evalImplementation(self, index = 0):
        try:
            if self.content.file is None:
                return None
            else:
                # check if file is png
                if self.content.file_path.endswith('png'):
                    img = read_image(self.content.file_path)
                    print(f"Image shape: {img.shape}")
                    self.markInvalid(False)
                    self.markDirty(False)
                    self.graphical_node.setToolTip(f"Shape: {img.shape}")
                    self.value = img
                    return self.value
                else:
                    self.markInvalid()
                    self.graphical_node.setToolTip("File type not supported")
                    return None        
        except Exception as e:print_traceback(e)

@register_node(OP_NODE_GETXYDATA)
class MLnode_getxydata(MLnode_node):
    icon = "icons/getdata.png"
    op_code = OP_NODE_GETXYDATA
    op_title = "getxydata"
    content_label = "getxydata"
    content_label_objname = "mlnode_node_getxydata"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[1, 1])

    def initInnerClasses(self):
        self.content = MLnode_getdata_content(self)
        self.graphical_node = MLnode_getdata_graphicsNode(self)
    

    def evalImplementation(self, index = 0):
        try:
            if self.content.file is None:
                return None
            else:
                self.value = MLnode_obj()
                if self.content.file_path.endswith('csv'):
                    data = pd.read_csv(self.content.file_path)
                    data = data.to_numpy(dtype=np.float32)
                    data = torch.from_numpy(data)
                    print(f"Data shape: {data.shape}")
                    y_col = int(self.content.y_col.text())
                    if y_col == -1:
                        y_col = data.shape[1]-1
                    self.value[0] = data[:, :y_col][0]
                    self.value[1] = data[:, y_col:][0]
                    self.markInvalid(False)
                    self.markDirty(False)
                    self.graphical_node.setToolTip(f"Shape: {data.shape}")
                    # self.value = data[0]
                    return self.value
                else:
                    self.markInvalid()
                    self.graphical_node.setToolTip("File type not supported")
                    return None        
        except Exception as e:print_traceback(e)

                

