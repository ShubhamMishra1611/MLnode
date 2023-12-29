import os
import typing
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect, Qt, QFile
from PyQt5.QtGui import QBrush, QColor, QPen, QFont, QPainter, QResizeEvent

from node_scene import scene, InvalidFile
from node_editor_graphics_view import Node_Editor_Graphics_View
from node_node import Node
from node_socket import Socket
from styles.style_node import NODE_EDITOR_STYLESHEET
from node_edge import Edge,EDGE_BEZIER, EGDE_DIRECT

class node_editor_widget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.stylesheet_filename = 'styles/nodestyle.qss'
        self.loadStylesheet(self.stylesheet_filename)
        self.file_name = None


        self.initUI()

    def is_file_name_set(self):
        return self.file_name is not None
    
    def get_user_friendly_file_name(self):
        name = os.path.basename(self.file_name) if self.is_file_name_set() else "New untitled Graph"
        return name
    
    def getSelectedItems(self):
        return self.scene.getSelectedItems()

    def hasSelectedItems(self):
        return self.getSelectedItems() != []

    def canUndo(self):
        return self.scene.history.canUndo()

    def canRedo(self):
        return self.scene.history.canRedo()


    def initUI(self):
        
        self.layout = QVBoxLayout() #TODO: should I go with VBox or HBox
        self.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.setStyleSheet(NODE_EDITOR_STYLESHEET)



        self.scene = scene()
        self.view = Node_Editor_Graphics_View(self.scene.grscene, self)
        self.layout.addWidget(self.view)


        self.add_node()
        

    def add_node(self):
        node_1 = Node(self.scene, "A Node 1", inputs = [1,2,3], outputs = [1])
        node_2 = Node(self.scene, "A Node 2", inputs = [1,2,2], outputs = [1])
        node_3 = Node(self.scene, "A Node 3", inputs = [1,2,3], outputs = [1])
        node_4 = Node(self.scene, "A Node 4", inputs = [1,2,3], outputs = [1])
        
        node_1.setPos(-250, -250)
        node_2.setPos(-150, 20)
        node_3.setPos(100, -80)
        node_4.setPos(500, -80)

        edge1 = Edge(self.scene, node_1.outputs[0], node_2.inputs[2], type_edge=EDGE_BEZIER)
        edge2 = Edge(self.scene, node_2.outputs[0], node_3.inputs[0], type_edge=EDGE_BEZIER)
        edge3 = Edge(self.scene, node_3.outputs[0], node_4.inputs[0], type_edge=EDGE_BEZIER)

        self.scene.history.storeInitialHistoryStamp()


    def loadStylesheet(self, filename):
        print('STYLE loading:', filename)
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))    

    def fileNew(self):
        self.scene.clear()
        self.file_name = None
        self.scene.history.clear()
        self.scene.history.storeInitialHistoryStamp()


    
    def fileload(self, file_name):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.scene.loadFromFile(file_name)
            self.file_name = file_name
            return True
        except InvalidFile as e:
            print(e)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, f'Error in loading the file {file_name} --- {e}', 'Error '*20, QMessageBox.Ok)
            return False
        finally:
            QApplication.restoreOverrideCursor()
    
    def fileSave(self, filename=None):
        # when called with empty parameter, we won't store the filename
        if filename is not None: self.file_name = filename
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.scene.saveToFile(self.file_name)
        QApplication.restoreOverrideCursor()
        return True

            



    def addDebugContent(self):
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)


        rect = self.grScene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)

        text = self.grScene.addText("This is my Awesome text!", QFont("Ubuntu"))
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))


        widget1 = QPushButton("Hello World")
        proxy1 = self.grScene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy1.setPos(0, 30)


        widget2 = QTextEdit()
        proxy2 = self.grScene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy2.setPos(0, 60)


        line = self.grScene.addLine(-200, -200, 400, -100, outlinePen)
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)




