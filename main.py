import sys
from PyQt5.QtWidgets import *

from nodeditor_wind import node_editor_wind

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = node_editor_wind()
    sys.exit(app.exec_())