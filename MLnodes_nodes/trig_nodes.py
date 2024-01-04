from MLnode_conf import *
from MLnode_node_base import *
from PyQt5.QtCore import *
from utility import print_traceback
import numpy as np

class MLNode_trignode_content(QNode_content_widget):
    def initUI(self):
        # have a combo box for the trig function
        self.combo = QComboBox(self)
        self.combo.addItem("sin")
        self.combo.addItem("cos")
        self.combo.addItem("tan")
        self.combo.addItem("csc")
        self.combo.addItem("sec")
        self.combo.addItem("cot")
        self.combo.setObjectName(self.node.content_label_objname)
        self.combo.setCurrentIndex(0)
    
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
        self.graphical_node = MLnode_graphicNode(self)
        self.content.combo.currentIndexChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        i1 = self.getInput(0)
        if i1 is None:
            self.markInvalid()
            self.markDescendantsDirty()
            self.graphical_node.setToolTip("Connect all inputs")
            return None
        else:
            active_trig_function = self.content.combo.currentText()
            if active_trig_function == "sin":
                val = np.sin(i1.eval())
            elif active_trig_function == "cos":
                val = np.cos(i1.eval())
            elif active_trig_function == "tan":
                val = np.tan(i1.eval())
            elif active_trig_function == "csc":
                val = 1/np.sin(i1.eval())
            elif active_trig_function == "sec":
                val = 1/np.cos(i1.eval())
            elif active_trig_function == "cot":
                val = 1/np.tan(i1.eval())
            else:
                self.markInvalid()
                self.markDescendantsDirty()
                self.graphical_node.setToolTip("Invalid trig function")
                return None
            self.value = val
            self.markDirty(False)
            self.markInvalid(False)
            self.graphical_node.setToolTip("")
            self.markDescendantsDirty()
            self.evalChildren()
            return val