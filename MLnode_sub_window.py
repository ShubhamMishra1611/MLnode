from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget
from node_editor_widget import node_editor_widget
from MLnode_conf import *
from MLnode_node_base import *
from utility import print_traceback


class mlnode_sub_window(node_editor_widget):
    def __init__(self) -> None:
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setTitle()

        self.scene.addDragEnterListener(self.onDragEnter)
        self.scene.addDropListener(self.onDrop)
        self.scene.setNodeClassSelector(self.getNodeClassFromData)


        self._close_event_listeners = []

    def getNodeClassFromData(self, data):
        if 'op_code' not in data: return Node
        return get_class_from_opcode(data['op_code'])



    def setTitle(self):
        self.setWindowTitle(self.get_user_friendly_file_name())

    def addCloseEventListener(self, callback):
        self._close_event_listeners.append(callback)

    def closeEvent(self, event):
        for callback in self._close_event_listeners: callback(self, event)

    def onDragEnter(self, event):
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event.acceptProposedAction()
        else:
            event.setAccepted(False)

    def onDrop(self, event):
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
            try:
                node = get_class_from_opcode(op_code)(self.scene)
                node.setPos(scene_position.x(), scene_position.y())
                self.scene.history.store_history(f'Created new node <{node.__class__.__name__}>')
            except Exception as e: print_traceback(e)
            # self.scene.add_node(node)


            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

