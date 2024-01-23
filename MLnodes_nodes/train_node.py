from MLnode_conf import *
from MLnode_node_base import *
from PyQt5.QtCore import *
from utility import print_traceback
import numpy as np
import torch
import json

class MLNode_trainnode_graphicsNode(MLnode_graphicNode):
    def initSizes(self):
        super().initSizes()
        self.width = 200
        self.height = 150

class MLnode_trainnode_content(QNode_content_widget):
    def initUI(self):
        self.layout = QGridLayout(self)
        self.epoch_edit = QLineEdit('100', self)
        self.optim_combo = QComboBox(self)
        self.optim_combo.addItems(['Adam', 'SGD'])
        self.optim_combo.setCurrentIndex(0)
        self.loss_combo = QComboBox(self)
        self.loss_combo.addItems(['MSE', 'CrossEntropy'])
        self.loss_combo.setCurrentIndex(0)
        self.lr_edit = QLineEdit('0.01', self)
        self.epoch_label = QLabel("Epoch", self)
        self.optim_label = QLabel("Optimizer", self)
        self.lr_label = QLabel("Learning rate", self)
        self.loss_label = QLabel("Loss function", self)

        self.epoch_edit.setObjectName(self.node.content_label_objname)
        self.optim_combo.setObjectName(self.node.content_label_objname)
        self.lr_edit.setObjectName(self.node.content_label_objname)
        self.loss_combo.setObjectName(self.node.content_label_objname)

        self.layout.addWidget(self.epoch_label, 0, 0)
        self.layout.addWidget(self.optim_label, 1, 0)
        self.layout.addWidget(self.lr_label, 2, 0)
        self.layout.addWidget(self.loss_label, 3, 0)

        self.layout.addWidget(self.epoch_edit, 0, 1)
        self.layout.addWidget(self.optim_combo, 1, 1)
        self.layout.addWidget(self.lr_edit, 2, 1)
        self.layout.addWidget(self.loss_combo, 3, 1)


    def serialize(self):
        res = super().serialize()
        res['value_epoch'] = self.epoch_edit.text()
        res['value_optim'] = self.optim_combo.currentIndex()
        res['value_lr'] = self.lr_edit.text()
        res['value_loss'] = self.loss_combo.currentIndex()
        return res
    
    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value_epoch = data['value_epoch']
            value_optim = data['value_optim']
            value_lr = data['value_lr']
            value_loss = data['value_loss']
            self.epoch_edit.setText(value_epoch)
            self.optim_combo.setCurrentIndex(value_optim)
            self.lr_edit.setText(value_lr)
            self.loss_combo.setCurrentIndex(value_loss)
            return True & res
        except Exception as e:print_traceback(e)
        return res
    
@register_node(OP_NODE_TRAINING)
class MLnode_trainnode(MLnode_node):
    icon = "icons/trainnode.png"
    op_code = OP_NODE_TRAINING
    op_title = "Training"
    content_label = "Training"
    content_label_objname = "mlnode_node_trainnode"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[])

    def initInnerClasses(self):
        self.content = MLnode_trainnode_content(self)
        self.graphical_node = MLNode_trainnode_graphicsNode(self)
        self.content.epoch_edit.textChanged.connect(self.onInputChanged)
        self.content.optim_combo.currentIndexChanged.connect(self.onInputChanged)
        self.content.lr_edit.textChanged.connect(self.onInputChanged)
        self.content.loss_combo.currentIndexChanged.connect(self.onInputChanged)

    def evalImplementation(self, index = 0):
        u_epoch = self.content.epoch_edit.text()
        u_optim = self.content.optim_combo.currentText()
        u_lr = self.content.lr_edit.text()
        u_loss = self.content.loss_combo.currentText()

        try:
            epoch = int(u_epoch)
            optim = u_optim
            lr = float(u_lr)
            loss = u_loss
            self.graphical_node.setToolTip(f"Training for {epoch} epochs with {optim} optimizer and {lr} learning rate")
            self.markDirty(False)
            self.markInvalid(False)
            training_config = {
                'epoch': epoch,
                'optim': optim,
                'lr': lr,
                'loss': loss
            }
            json.dump(training_config, open('temp/training_config.json', 'w'))

        except:
            self.markInvalid()
            self.markDescendantsDirty()
            self.graphical_node.setToolTip("Invalid input(s)!")
            return None
        return None
    
    def onInputChanged(self):
        self.markDirty()
        self.eval()