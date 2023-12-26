import sys
from PyQt5.QtWidgets import *

from MLnode_window import MLnodeWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = MLnodeWindow()
    wnd.show()
    sys.exit(app.exec_())