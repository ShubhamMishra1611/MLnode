import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from node_editor_widget import node_editor_widget

class node_editor_window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.name_company = 'MLnode'
        self.name_product = 'MLnode'
        self.filename = None
        self.init_UI()

    def init_UI(self):
        self.node_editor = node_editor_widget(self)
        self.setCentralWidget(self.node_editor)
        
        self.createActions()
        self.createMenus()

        self.createStatusBar()


        self.setGeometry(200, 200, 800, 600) # setting the geometry

        self.setWindowTitle("Node Editor") # setting window title
        self.show()

    def createStatusBar(self):
        self.statusBar().showMessage('')
        self.status_mouse_pos = QLabel('')
        self.statusBar().addPermanentWidget(self.status_mouse_pos)
        self.node_editor.view.scene_pos_changed.connect(self.on_scene_pos_changed)

    
    def createActions(self):
        self.actNew = QAction('&New', self, shortcut='Ctrl+N', statusTip="Create new graph", triggered=self.on_file_new)
        self.actOpen = QAction('&Open', self, shortcut='Ctrl+O', statusTip="Open file", triggered=self.on_file_open)
        self.actSave = QAction('&Save', self, shortcut='Ctrl+S', statusTip="Save file", triggered=self.on_file_save)
        self.actSaveAs = QAction('Save &As...', self, shortcut='Ctrl+Shift+S', statusTip="Save file as...", triggered=self.on_file_save_as)
        self.actExit = QAction('E&xit', self, shortcut='Ctrl+Q', statusTip="Exit application", triggered=self.close)

        self.actUndo = QAction('&Undo', self, shortcut='Ctrl+Z', statusTip="Undo last operation", triggered=self.on_undo)
        self.actRedo = QAction('&Redo', self, shortcut='Ctrl+Shift+Z', statusTip="Redo last operation", triggered=self.on_redo)
        self.actDelete = QAction('&Delete', self, shortcut='Del', statusTip="Delete selected items", triggered=self.on_delete)

    def createMenus(self):
        menubar = self.menuBar()

        self.fileMenu = menubar.addMenu('&File')
        self.fileMenu.addAction(self.actNew)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actOpen)
        self.fileMenu.addAction(self.actSave)
        self.fileMenu.addAction(self.actSaveAs)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actExit)

        self.editMenu = menubar.addMenu('&Edit')
        self.editMenu.addAction(self.actUndo)
        self.editMenu.addAction(self.actRedo)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actDelete)

    def on_scene_pos_changed(self, x, y):
        self.status_mouse_pos.setText(f'[{x}, {y}]')
    
    def on_file_new(self):
        self.get_current_node_editor_widget().fileNew()

    def on_file_open(self):
        file_name, filter = QFileDialog.getOpenFileName(self, 'Open graph from file')

        if file_name == '':
            return
        if os.path.isfile(file_name):
            self.get_current_node_editor_widget().scene.loadFromFile(file_name)


    def on_file_save(self):
        current_nodeeditor = self.get_current_node_editor_widget()
        if current_nodeeditor is not None:
            if not current_nodeeditor.is_file_name_set(): return self.on_file_save_as()

            current_nodeeditor.fileSave()
            self.statusBar().showMessage("Successfully saved %s" % current_nodeeditor.file_name, 5000)

            return True


    def on_file_save_as(self):
        current_nodeeditor = self.get_current_node_editor_widget()
        if current_nodeeditor is not None:
            fname, filter = QFileDialog.getSaveFileName(self, 'Save graph to file')
            if fname == '': return False

            current_nodeeditor.fileSave(fname)
            self.statusBar().showMessage("Successfully saved as %s" % current_nodeeditor.file_name, 5000)

            return True



    def on_undo(self):
        if self.get_current_node_editor_widget():
            self.get_current_node_editor_widget().scene.history.undo()

    def on_redo(self):
        if self.get_current_node_editor_widget():
            self.get_current_node_editor_widget().scene.history.redo()


    def on_delete(self):
        if self.get_current_node_editor_widget():
            self.get_current_node_editor_widget().scene.grscene.views()[0].delete_selected()
        

    def get_current_node_editor_widget(self):
        return self.centralWidget()
    
    def close(self) -> bool:
        return super().close()
    
    def readSettings(self):
        settings = QSettings(self.name_company, self.name_product)
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        settings = QSettings(self.name_company, self.name_product)
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())
