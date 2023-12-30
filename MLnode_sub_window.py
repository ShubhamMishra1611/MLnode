from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget
from node_editor_widget import node_editor_widget
from MLnode_conf import *
from MLnode_node_base import *


class mlnode_sub_window(node_editor_widget):
    def __init__(self) -> None:
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setTitle()

        self.scene.addDragEnterListener(self.onDragEnter)
        self.scene.addDropListener(self.onDrop)


        self._close_event_listeners = []


    def setTitle(self):
        self.setWindowTitle(self.get_user_friendly_file_name())

    def addCloseEventListener(self, callback):
        self._close_event_listeners.append(callback)

    def closeEvent(self, event):
        for callback in self._close_event_listeners: callback(self, event)

    def onDragEnter(self, event):
        # print("CalcSubWnd :: ~onDragEnter")
        # print("text: '%s'" % event.mimeData().text())
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event.acceptProposedAction()
        else:
            # print(" ... denied drag enter event")
            event.setAccepted(False)

    def onDrop(self, event):
        # print("CalcSubWnd :: ~onDrop")
        # print("text: '%s'" % event.mimeData().text())
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            eventData = event.mimeData().data(LISTBOX_MIMETYPE)
            dataStream = QDataStream(eventData, QIODevice.ReadOnly)
            pixmap = QPixmap()
            dataStream >> pixmap 
            op_code = dataStream.readInt()
            text = dataStream.readQString()

            mouse_position = event.pos()
            scene_position = self.scene.grscene.views()[0].mapToScene(mouse_position)

            print("GOT DROP: [%d] '%s'" % (op_code, text), "mouse:", mouse_position, "scene:", scene_position)


            # @TODO Fix me!
            # node = MLnode_node(self.scene, text, inputs=[1,1], outputs=[2])
            node = MLnode_node(self.scene, op_code, text, inputs=[1,1], outputs=[2])
            node.setPos(scene_position.x(), scene_position.y())
            # self.scene.add_node(node)


            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

