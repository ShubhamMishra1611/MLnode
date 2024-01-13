from MLnode_conf import *
from MLnode_node_base import *
from PyQt5.QtCore import *
from utility import print_traceback
import numpy as np
import torch
import pandas as pd
import glob
import os


class MLnode_getdata_graphicsNode(MLnode_graphicNode):
    def initSizes(self):
        super().initSizes()
        self.width = 150
        self.height = 100

class MLnode_getdata_content(QNode_content_widget):
    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.label_file_name = QLabel("File location (csv)")

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
    
    def evalImplementation(self):
        try:
            if self.content.file is None:
                return None
            else:
                # check if file is csv
                if self.content.file_path.endswith('csv'):
                    data = pd.read_csv(self.content.file_path)
                    data = data.to_numpy(dtype=np.float32)
                    data = torch.from_numpy(data)
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

                

