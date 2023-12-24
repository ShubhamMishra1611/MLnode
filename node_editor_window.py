import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from node_editor_widget import node_editor_widget

class node_editor_window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.init_UI()
        self.file_name = None

    def create_act(self, name, shortcut, tooltip, callback):
        act = QAction(name, self)
        act.setShortcut(shortcut)
        act.setToolTip(tooltip)
        act.triggered.connect(callback)
        return act

    def init_UI(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(self.create_act('&New', 'Ctrl+N', 'Create a New Graph', self.on_file_new))
        file_menu.addSeparator()
        file_menu.addAction(self.create_act('&Open', 'Ctrl+O', 'Open file', self.on_file_open))
        file_menu.addAction(self.create_act('&Save', 'Ctrl+S', 'Save file', self.on_file_save))
        file_menu.addAction(self.create_act('Save &As..', 'Ctrl+Shift+S', 'Save file as...', self.on_file_save_as))
        file_menu.addSeparator()
        file_menu.addAction(self.create_act('E&xit', 'Ctrl+Q', 'Exit Application', self.close))

        edit_menu = menu_bar.addMenu('&Edit')
        edit_menu.addAction(self.create_act('&Undo', 'Ctrl+Z', 'Undo the last operation', self.on_undo))
        edit_menu.addAction(self.create_act('&Redo', 'Ctrl+Shift+Z', 'Redo the last operation', self.on_redo))
        edit_menu.addSeparator()
        edit_menu.addAction(self.create_act('&Delete', 'Del', 'Delete the selected item', self.on_delete))
        


        node_editor = node_editor_widget(self)
        self.setCentralWidget(node_editor)

        self.statusBar().showMessage('')
        self.status_mouse_pos = QLabel('')
        self.statusBar().addPermanentWidget(self.status_mouse_pos)
        node_editor.view.scene_pos_changed.connect(self.on_scene_pos_changed)


        self.setGeometry(200, 200, 800, 600) # setting the geometry

        self.setWindowTitle("Node Editor") # setting window title
        self.show()

    def on_scene_pos_changed(self, x, y):
        self.status_mouse_pos.setText(f'[{x}, {y}]')
    
    def on_file_new(self):
        self.centralWidget().scene.clear()

    def on_file_open(self):
        file_name, filter = QFileDialog.getOpenFileName(self, 'Open graph from file')

        if file_name == '':
            return
        if os.path.isfile(file_name):
            self.centralWidget().scene.loadFromFile(file_name)


    def on_file_save(self):
        if self.file_name is None: return self.on_file_save_as()
        self.centralWidget().scene.saveToFile(self.file_name)
        self.statusBar().showMessage(f'Successfully saved file name as {self.file_name}')

    def on_file_save_as(self):
        file_name, filter = QFileDialog.getSaveFileName(self, 'Save graph to file')
        print("on file save as clicked")
        self.file_name = file_name
        self.on_file_save()

    def on_undo(self):
        self.centralWidget().scene.history.undo()

    def on_redo(self):
        self.centralWidget().scene.history.redo()


    def on_delete(self):
        self.centralWidget().scene.grscene.views()[0].delete_selected()
        

    def close(self) -> bool:
        return super().close()