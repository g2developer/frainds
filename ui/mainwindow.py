# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.testButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.testButton.setObjectName("testButton")
        self.gridLayout.addWidget(self.testButton, 0, 0, 1, 1)
        self.webEngineView = QtWebEngineWidgets.QWebEngineView(parent=self.centralwidget)
        self.webEngineView.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView.setObjectName("webEngineView")
        self.gridLayout.addWidget(self.webEngineView, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 807, 26))
        self.menubar.setObjectName("menubar")
        self.menuChat = QtWidgets.QMenu(parent=self.menubar)
        self.menuChat.setObjectName("menuChat")
        self.menuType = QtWidgets.QMenu(parent=self.menuChat)
        self.menuType.setObjectName("menuType")
        MainWindow.setMenuBar(self.menubar)
        self.actionchat1 = QtGui.QAction(parent=MainWindow)
        self.actionchat1.setObjectName("actionchat1")
        self.actionchat2 = QtGui.QAction(parent=MainWindow)
        self.actionchat2.setObjectName("actionchat2")
        self.menuChat.addAction(self.menuType.menuAction())
        self.menubar.addAction(self.menuChat.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "frainds"))
        self.testButton.setText(_translate("MainWindow", "PushButton"))
        self.menuChat.setTitle(_translate("MainWindow", "Chat"))
        self.menuType.setTitle(_translate("MainWindow", "Type"))
        self.actionchat1.setText(_translate("MainWindow", "chat1"))
        self.actionchat2.setText(_translate("MainWindow", "chat2"))
from PyQt6 import QtWebEngineWidgets


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())