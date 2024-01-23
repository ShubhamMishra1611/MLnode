from MLnode_conf import *
from MLnode_node_base import *
from PyQt5.QtCore import *
from utility import print_traceback
import numpy as np
import torch

class MLNode_trignode_graphicNode(MLnode_graphicNode):
    def initSizes(self):
        super().initSizes()
        self.width = 90
        self.height = 100
        self.title_height = 50.0

class MLNode_trignode_content(QNode_content_widget):
    def initUI(self):
        self.combo = QComboBox(self)
        self.combo.addItem("sin")
        self.combo.addItem("cos")
        self.combo.addItem("tan")
        self.combo.addItem("csc")
        self.combo.addItem("sec")
        self.combo.addItem("cot")
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


@register_node(OP_NODE_TRIG)
class MLNode_Trig(MLnode_node):
    icon = "icons/sin.png"
    op_code = OP_NODE_TRIG
    op_title = "Trig function"
    content_label = "sin"
    content_label_objname = "mlnode_node_trig"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def initInnerClasses(self):
        self.content = MLNode_trignode_content(self)
        self.graphical_node = MLNode_trignode_graphicNode(self)
        self.content.combo.currentIndexChanged.connect(self.onInputChanged)

    def evalImplementation(self, index = 0):
        i1 = self.getInput(0)
        if i1 is None:
            self.markInvalid()
            self.markDescendantsDirty()
            self.graphical_node.setToolTip("Connect all inputs")
            return None
        else:
            active_trig_function = self.content.combo.currentText()
            if active_trig_function == "sin":
                val = torch.sin(i1.eval())
            elif active_trig_function == "cos":
                val = torch.cos(i1.eval())
            elif active_trig_function == "tan":
                val = torch.tan(i1.eval())
            elif active_trig_function == "csc":
                val = 1/torch.sin(i1.eval())
            elif active_trig_function == "sec":
                val = 1/torch.cos(i1.eval())
            elif active_trig_function == "cot":
                val = 1/torch.tan(i1.eval())
            else:
                self.markInvalid()
                self.markDescendantsDirty()
                self.graphical_node.setToolTip("Invalid trig function")
                return None
            self.value[index] = val
            self.markDirty(False)
            self.markInvalid(False)
            self.graphical_node.setToolTip("")
            self.markDescendantsDirty()
            self.evalChildren()
            return self.value