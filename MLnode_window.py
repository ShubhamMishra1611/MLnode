from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from node_editor_window import node_editor_window
class MLnodeWindow(node_editor_window):
#     def __init__(self, parent: QWidget = None) -> None:
#         super().__init__()
#         self.initUI()

    def init_UI(self):
        self.name_company = 'MLnode'
        self.name_product = 'MLnode'

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

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()

        self.createNodesDock()

        self.readSettings()

        self.setWindowTitle("MLnode")

    def createActions(self):
        super().createActions()

        self.closeAct = QAction("Cl&ose", self,statusTip="Close the active window",triggered=self.mdiArea.closeActiveSubWindow)

        self.closeAllAct = QAction("Close &All", self,statusTip="Close all the windows",triggered=self.mdiArea.closeAllSubWindows)

        self.tileAct = QAction("&Tile", self, statusTip="Tile the windows",triggered=self.mdiArea.tileSubWindows)

        self.cascadeAct = QAction("&Cascade", self,statusTip="Cascade the windows",triggered=self.mdiArea.cascadeSubWindows)

        self.nextAct = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild,statusTip="Move the focus to the next window",
                triggered=self.mdiArea.activateNextSubWindow)

        self.previousAct = QAction("Pre&vious", self,shortcut=QKeySequence.PreviousChild,statusTip="Move the focus to the previous window",
                triggered=self.mdiArea.activatePreviousSubWindow)

        self.separatorAct = QAction(self)
        self.separatorAct.setSeparator(True)

        self.aboutAct = QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QApplication.instance().aboutQt)
    def createMenus(self):
        super().createMenus()

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)
    
    def createNodesDock(self):
        self.listWidget = QListWidget()
        self.listWidget.addItem("Transpose")
        self.listWidget.addItem("Unit Matrix")
        self.listWidget.addItem("Dot Product")
        self.listWidget.addItem("Matmul")

        self.items = QDockWidget("Nodes")
        self.items.setWidget(self.listWidget)
        self.items.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.items)


    def createToolBars(self):
        # self.fileToolBar = self.addToolBar("File")
        # self.fileToolBar.addAction(self.newAct)
        # self.fileToolBar.addAction(self.openAct)
        # self.fileToolBar.addAction(self.saveAct)

        # self.editToolBar = self.addToolBar("Edit")
        # self.editToolBar.addAction(self.cutAct)
        # self.editToolBar.addAction(self.copyAct)
        # self.editToolBar.addAction(self.pasteAct)
        pass

    def updateWindowMenu(self):
        self.windowMenu.clear()
        self.windowMenu.addAction(self.closeAct)
        self.windowMenu.addAction(self.closeAllAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.tileAct)
        self.windowMenu.addAction(self.cascadeAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.nextAct)
        self.windowMenu.addAction(self.previousAct)
        self.windowMenu.addAction(self.separatorAct)

        windows = self.mdiArea.subWindowList()
        self.separatorAct.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.userFriendlyCurrentFile())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.activeMdiChild())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)
    
    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def updateMenus(self):
        pass
    
    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()

    def readSettings(self):
        settings = QSettings('Trolltech', 'MDI Example')
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        self.move(pos)
        self.resize(size)
    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)

    def about(self):
        QMessageBox.about(self, "About MLnode",
                "The <b>MLnode</b> is a tool for create ML/DL nodes visually. "
                "For more information got to "
                "<a href='https://github.com/ShubhamMishra1611/MLnode'>MLnode github</a>")

        
    def updateWindowMenu(self):
        pass

    


    

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainWin = MLnodeWindow()
    mainWin.show()
    sys.exit(app.exec_())

    

    