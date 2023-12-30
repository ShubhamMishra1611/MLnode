from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class QDragListbox(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # init
        self.setIconSize(QSize(32, 32))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)

        self.addMyItems()


    def addMyItems(self):
        self.addMyItem("Input", "icons/unit_mat.png")
        self.addMyItem("Output", "icons/output.png")
        self.addMyItem("Add", "icons/add_mat.png")
        self.addMyItem("MatMul", "icons/mat_mul.png")
        self.addMyItem("Transpose", "icons/mat_transpose.png")
        self.addMyItem("Scalar", "icons/scalar_num.png")

    def addMyItem(self, name, icon=None, op_code=0):
        item = QListWidgetItem(name, self) # can be (icon, text, parent, <int>type)
        pixmap = QPixmap(icon if icon is not None else ".")
        item.setIcon(QIcon(pixmap))
        item.setSizeHint(QSize(32, 32))

        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        # setup data
        item.setData(Qt.UserRole, pixmap)
        item.setData(Qt.UserRole + 1, op_code)
