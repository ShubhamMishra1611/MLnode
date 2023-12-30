from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget
from node_editor_widget import node_editor_widget


class mlnode_sub_window(node_editor_widget):
    def __init__(self) -> None:
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setTitle()

        self._close_event_listeners = []


    def setTitle(self):
        self.setWindowTitle(self.get_user_friendly_file_name())

    def addCloseEventListener(self, callback):
        self._close_event_listeners.append(callback)

    def closeEvent(self, event):
        for callback in self._close_event_listeners: callback(self, event)
