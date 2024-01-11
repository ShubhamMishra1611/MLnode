import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from node_editor_window import node_editor_window
from MLnode_sub_window import mlnode_sub_window
from MLnode_listbox_drag import QDragListbox
from MLnode_conf import *
# from MLnode_conf_nodes import *
from pprint import pprint as pp 
from utility import print_traceback

DEBUG = False

class MLnodeWindow(node_editor_window):

    def init_UI(self):
        self.name_company = 'MLnode'
        self.name_product = 'MLnode'

        self.empty_icon = QIcon(".")
        if DEBUG:
            print("Registered nodes:")
            pp(MLNODE_NODES)
        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.mdiArea.setDocumentMode(True)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.createNodesDock()
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()


        self.readSettings()

        self.setWindowTitle("MLnode")

    def createActions(self):
        super().createActions()

        self.actClose = QAction("Cl&ose", self,statusTip="Close the active window",triggered=self.mdiArea.closeActiveSubWindow)

        self.actCloseAll = QAction("Close &All", self,statusTip="Close all the windows",triggered=self.mdiArea.closeAllSubWindows)

        self.actTile = QAction("&Tile", self, statusTip="Tile the windows",triggered=self.mdiArea.tileSubWindows)

        self.actModelRegister = QAction("&Register", self, statusTip="Register the model",triggered=self.on_model_register)

        self.actCascade = QAction("&Cascade", self,statusTip="Cascade the windows",triggered=self.mdiArea.cascadeSubWindows)

        self.actNext = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild,statusTip="Move the focus to the next window",
                triggered=self.mdiArea.activateNextSubWindow)

        self.actPrevious = QAction("Pre&vious", self,shortcut=QKeySequence.PreviousChild,statusTip="Move the focus to the previous window",
                triggered=self.mdiArea.activatePreviousSubWindow)

        self.actSeparator = QAction(self)
        self.actSeparator.setSeparator(True)

        self.aboutAct = QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QApplication.instance().aboutQt)
    
    def on_file_new(self):
        try:
            subwindow = self.create_mdi_child()
            subwindow.widget().fileNew()
            subwindow.show()
        except Exception as e: print_traceback(e)

    
    def on_file_open(self):
        file_names, filter = QFileDialog.getOpenFileNames(self, 'Open graph from file')

        try:
            for file_name in file_names:
                if file_name:
                    existing = self.findMdiChild(file_name)
                    if existing:
                        self.mdiArea.setActiveSubWindow(existing)
                    else:
                        node_editor = mlnode_sub_window()
                        if node_editor.fileload(file_name): 
                            self.statusBar().showMessage(f'File {file_name} is loaded', 5000)
                            node_editor.setTitle()
                            subwindow = self.create_mdi_child(node_editor)
                            subwindow.show()
                        else:
                            node_editor.close()
        except Exception as e: print_traceback(e)
                

    
    def create_mdi_child(self, child_widget = None):
        node_editor = child_widget if child_widget is not None else mlnode_sub_window()
        subwindow = self.mdiArea.addSubWindow(node_editor)
        subwindow.setWindowIcon(self.empty_icon)
        node_editor.scene.history.addHistoryModifiedListener(self.updateEditMenu)
        node_editor.addCloseEventListener(self.onSubWndClose)
        return subwindow
    
    def onSubWndClose(self, widget, event):
        existing = self.findMdiChild(widget.file_name)
        self.mdiArea.setActiveSubWindow(existing)

        event.accept()
        # if self.maybeSave(): # TODO: implement maybeSave
        #     event.accept()
        # else:
        #     event.ignore()

    
    def findMdiChild(self, file_name):

        for window in self.mdiArea.subWindowList():
            if window.widget().file_name == file_name:
                return window
        return None
    
    def createMenus(self):
        super().createMenus()

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)
        self.editMenu.aboutToShow.connect(self.updateEditMenu)

    def createNodesDock(self):
        self.nodesListWidget = QDragListbox()

        self.nodesDock = QDockWidget("Nodes")
        self.nodesDock.setWidget(self.nodesListWidget)
        self.nodesDock.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.nodesDock)


    def createToolBars(self):
        pass

    def on_model_register(self):
        all_nodes  = None
        current_nodeeditor = self.get_current_node_editor_widget()
        if current_nodeeditor is not None:
            all_nodes = current_nodeeditor.scene.nodes

        for node in all_nodes:
            print(node.getImplemClassInstance())

    def updateWindowMenu(self):
        self.windowMenu.clear()
        toolbar_nodes = self.windowMenu.addAction("Nodes Toolbar")
        toolbar_nodes.setCheckable(True)
        toolbar_nodes.triggered.connect(self.onWindowNodesToolbar)
        toolbar_nodes.setChecked(self.nodesDock.isVisible())

        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actClose)
        self.windowMenu.addAction(self.actCloseAll)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actTile)
        self.windowMenu.addAction(self.actCascade)
        self.windowMenu.addAction(self.actModelRegister)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actNext)
        self.windowMenu.addAction(self.actPrevious)
        self.windowMenu.addAction(self.actSeparator)

        windows = self.mdiArea.subWindowList()
        self.actSeparator.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.get_user_friendly_file_name())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.get_current_node_editor_widget())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)
    
    def onWindowNodesToolbar(self):
        if self.nodesDock.isVisible():
            self.nodesDock.hide()
        else:
            self.nodesDock.show()

    
    def activeMdiChild(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None
    
    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def get_current_node_editor_widget(self):
        """ we're returning NodeEditorWidget here... """
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    
    def updateMenus(self):
        active = self.get_current_node_editor_widget()
        hasMdiChild = (active is not None)

        self.actSave.setEnabled(hasMdiChild)
        self.actSaveAs.setEnabled(hasMdiChild)
        self.actClose.setEnabled(hasMdiChild)
        self.actCloseAll.setEnabled(hasMdiChild)
        self.actTile.setEnabled(hasMdiChild)
        self.actCascade.setEnabled(hasMdiChild)
        self.actNext.setEnabled(hasMdiChild)
        self.actPrevious.setEnabled(hasMdiChild)
        self.actSeparator.setVisible(hasMdiChild)

        self.updateEditMenu()

    def updateEditMenu(self):
        try:
            active = self.get_current_node_editor_widget()
            hasMdiChild = (active is not None)
            self.actDelete.setEnabled(hasMdiChild and active.hasSelectedItems())

            self.actUndo.setEnabled(hasMdiChild and active.canUndo())
            self.actRedo.setEnabled(hasMdiChild and active.canRedo())
        except Exception as e: print_traceback(e)


    
    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()
    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)

    def about(self):
        QMessageBox.about(self, "About MLnode",
                "The <b>MLnode</b> is a tool for create ML/DL nodes visually. "
                "For more information got to "
                "<a href='https://github.com/ShubhamMishra1611/MLnode'>MLnode github</a>")

        

    


    

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainWin = MLnodeWindow()
    mainWin.show()
    sys.exit(app.exec_())

    

    