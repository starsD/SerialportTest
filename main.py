import Unity_mainFrame
import os
from PyQt5 import QtCore, QtGui, QtWidgets

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    SerialTest = QtWidgets.QMainWindow()
    ui = Unity_mainFrame.UnitySerialTest(SerialTest)
    SerialTest.show()
    os._exit(app.exec_())
