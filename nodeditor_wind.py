import typing
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect, Qt, QFile
from PyQt5.QtGui import QBrush, QColor, QPen, QFont, QPainter, QResizeEvent

from node_scene import scene
from node_editor_graphics_view import Node_Editor_Graphics_View
from node_node import Node
from node_socket import Socket
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
        node = Node(self.scene, "A Node", inputs = [1,1,1], outputs = [1])

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




