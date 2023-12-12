import typing
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect, Qt, QFile
from PyQt5.QtGui import QBrush, QColor, QPen, QFont, QPainter, QResizeEvent

from node_scene import scene
from node_editor_graphics_view import Node_Editor_Graphics_View
from node_node import Node
from styles.style_node import NODE_EDITOR_STYLESHEET

class node_editor_wind(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.stylesheet_filename = 'styles/nodestyle.qss'
        self.loadStylesheet(self.stylesheet_filename)


        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 800, 600) # setting the geometry

        self.layout = QVBoxLayout() #TODO: should I go with VBox or HBox
        self.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.setStyleSheet(NODE_EDITOR_STYLESHEET)



        self.scene = scene()
        node = Node(self.scene, "A Node")

        self.view = Node_Editor_Graphics_View(self.scene.grscene, self)
        self.layout.addWidget(self.view)


        self.setWindowTitle("Node Editor") # setting window title
        self.show()
        # self.addDebugContent()

    def loadStylesheet(self, filename):
        print('STYLE loading:', filename)
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))


    def addDebugContent(self):
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)

        rect = self.scene.grscene.addRect(0, 0, 80, 100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)

        text = self.scene.grscene.addText("This is something random!", QFont("Ubuntu"))
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))






