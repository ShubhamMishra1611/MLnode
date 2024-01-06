import sys
from PyQt5.QtWidgets import *

from node_editor_window import node_editor_window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = node_editor_window()
    sys.exit(app.exec_())