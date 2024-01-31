from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from node_node import Node
from node_content_widget import QNode_content_widget
from node_graphics import QgraphicsNode
from node_socket import LEFT_CENTER, RIGHT_CENTER
from utility import print_traceback
import numpy as np
from MLnode_object import MLnode_obj

class MLnode_graphicNode(QgraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 74
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

    def initAssets(self):
        super().initAssets()
        self.icons = QImage("icons/status_icons.png")

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

        offset = 24.0
        if self.node.isDirty(): offset = 0.0
        if self.node.isInvalid(): offset = 48.0
        if self.node.isGrad(): 
            self.icons = QImage('icons\grad.png')
            offset = 0.0
        if self.node.get_device_type() == 'GPU':
            self.icons = QImage('icons\GPU.png')
            offset = 0.0


        painter.drawImage(
            QRectF(-10, -10, 24.0, 24.0),
            self.icons,
            QRectF(offset, 0, 24.0, 24.0)
        )


class MLnode_content(QNode_content_widget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)

class MLnode_node(Node):
    icon = ""
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "mlnode_node_bg"

    def __init__(self, scene, inputs=None, outputs=None) -> None:
        if inputs is None:
            inputs = [2,2]
        if outputs is None:
            outputs = [1]

        super().__init__(scene, self.__class__.op_title, inputs, outputs)
        self.value = MLnode_obj()
        self.markDirty()

    def evalOperation(self, input1, input2):
        return np.array([0])
    
    def evalMethod(self, input1, input2):
        return np.array([0])

    def evalImplementation(self, index = 0):
        raise NotImplementedError
        i1 = self.getInput(0)
        i2 = self.getInput(1)

        if i1 is None or i2 is None:
            self.markInvalid()
            self.markDescendantsDirty()
            self.graphical_node.setToolTip("Connect all inputs")
            return None

        else:
            val = self.evalOperation(i1.eval(), i2.eval())
            self.value = val
            self.markDirty(False)
            self.markInvalid(False)
            self.graphical_node.setToolTip("")

            self.markDescendantsDirty()
            self.evalChildren()

            return val

   
    def eval(self, index=0):
        if not self.isDirty() and not self.isInvalid():
            print(f'_> returning cache {self.__class__.__name__} value as {self.value}')
            return self.value[index]
        try:
            val = self.evalImplementation(index)
            return val[index]
        except ValueError as e:
            self.markInvalid()
            self.graphical_node.setToolTip(str(e))
            self.markDescendantsDirty()
        except Exception as e:
            self.markInvalid()
            self.graphical_node.setToolTip(str(e))
            print_traceback(e)
    
    def onInputChanged(self, new_edge):
        print(f'onInputChanged')
        self.markDirty()
        self.eval()

    def initInnerClasses(self):
        self.content = MLnode_content(self)
        self.graphical_node = MLnode_graphicNode(self)

    def initSettings(self):
        super().initSettings()
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER

    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        return res
    
    def getImplemClassInstance(self):
        return None



