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
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(9, -1, 9, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout.addWidget(self.checkBox)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.webEngineView = QtWebEngineWidgets.QWebEngineView(parent=self.centralwidget)
        self.webEngineView.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView.setObjectName("webEngineView")
        self.gridLayout.addWidget(self.webEngineView, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuChat = QtWidgets.QMenu(parent=self.menubar)
        self.menuChat.setObjectName("menuChat")
        self.menuType = QtWidgets.QMenu(parent=self.menuChat)
        self.menuType.setObjectName("menuType")
        self.menuVoice = QtWidgets.QMenu(parent=self.menubar)
        self.menuVoice.setObjectName("menuVoice")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.actionchat1 = QtGui.QAction(parent=MainWindow)
        self.actionchat1.setObjectName("actionchat1")
        self.actionchat2 = QtGui.QAction(parent=MainWindow)
        self.actionchat2.setObjectName("actionchat2")
        self.actionVoice_recognition = QtGui.QAction(parent=MainWindow)
        self.actionVoice_recognition.setCheckable(True)
        self.actionVoice_recognition.setChecked(True)
        self.actionVoice_recognition.setObjectName("actionVoice_recognition")
        self.actionkeep_going_chat = QtGui.QAction(parent=MainWindow)
        self.actionkeep_going_chat.setCheckable(True)
        self.actionkeep_going_chat.setObjectName("actionkeep_going_chat")
        self.actionExit = QtGui.QAction(parent=MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuChat.addAction(self.menuType.menuAction())
        self.menuVoice.addAction(self.actionVoice_recognition)
        self.menuVoice.addAction(self.actionkeep_going_chat)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuVoice.menuAction())
        self.menubar.addAction(self.menuChat.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "frainds"))
        self.checkBox.setText(_translate("MainWindow", "keep chat going"))
        self.menuChat.setTitle(_translate("MainWindow", "Chat"))
        self.menuType.setTitle(_translate("MainWindow", "Type"))
        self.menuVoice.setTitle(_translate("MainWindow", "Voice"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionchat1.setText(_translate("MainWindow", "chat1"))
        self.actionchat2.setText(_translate("MainWindow", "chat2"))
        self.actionVoice_recognition.setText(_translate("MainWindow", "Voice recognition"))
        self.actionkeep_going_chat.setText(_translate("MainWindow", "Keep going Chat"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
from PyQt6 import QtWebEngineWidgets


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
