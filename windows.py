import time
from threading import Timer

import clipboard
import pyautogui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtNetwork import QNetworkCookie
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineCookieStore, QWebEngineProfile, qWebEngineChromiumVersion

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtWebEngineWidgets import QWebEngineView

from PyQt6 import uic, QtGui, QtCore

from ui.mainwindow import Ui_MainWindow


def setTimeout(fn, ms, *args, **kwargs):
    t = Timer(ms / 1000., fn, args=args, kwargs=kwargs)
    t.start()
    return t


# class MainWindow(QMainWindow, form_class):
class MainWindow(QMainWindow):
    webEngineProfile = None
    webEngineView: QWebEngineView = None

    chatai_list = None
    chatai = 'chatGPT'
    chatai_url = 'https://chat.openai.com/'

    dataAcc = None

    tempMousePosition = None

    def __init__(self, data_acc):
        super().__init__()
        # self.setupUi(self)
        self.dataAcc = data_acc
        self.set_chatai()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.set_menu()

        self.webEngineView = self.ui.webEngineView

        # self.webEngineProfile = QWebEngineProfile.defaultProfile()
        self.webEngineProfile = QWebEngineProfile('frainds')
        self.webEngineProfile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        # profile.setCachePath(QStandardPaths.writableLocation(self, QStandardPaths.StandardLocation))
        # profile.setPersistentStoragePath(QStandardPaths.writableLocation(self, QStandardPaths.StandardLocation))

        # print('persistentCookiesPolicy ', self.webEngineProfile.persistentCookiesPolicy())
        # print(self.webEngineProfile.persistentCookiesPolicy(), self.webEngineProfile.isOffTheRecord())
        #
        # print('cachePath ' + self.webEngineProfile.cachePath())
        # print('persistentStoragePath ' + self.webEngineProfile.persistentStoragePath())

        page: QWebEnginePage = QWebEnginePage(self.webEngineProfile, self)
        self.webEngineView.setPage(page)
        # webview.loadFinished.connect(self.loadFinished)

        self.ui.testButton.clicked.connect(lambda : self.searchAi('소프트웨어의 정의에 대해서 찾아줘'))

    def set_chatai(self):
        if self.dataAcc:
            self.chatai = self.dataAcc.get_config_value('chatai')
            self.chatai_url = self.dataAcc.get_config_option('chatai', self.chatai)

    def set_menu(self):
        _translate = QtCore.QCoreApplication.translate
        self.ui.menuType.setTitle(_translate("MainWindow", self.chatai))
        self.dataAcc.get_config_option('chatai', self.chatai)
        self.chatai_list = self.dataAcc.get_config_option('chatai')
        for (idx, row) in enumerate(self.chatai_list):
            action = QtGui.QAction(parent=self)
            action.setObjectName(row[1])
            action.setText(_translate("MainWindow", row[1]))
            action.triggered.connect(lambda chk, item=row: self.change_chatai(item))
            self.ui.menuType.addAction(action)

    def change_chatai(self, item):
        # print(action)
        _translate = QtCore.QCoreApplication.translate
        self.chatai = item[1]
        self.chatai_url = item[2]
        print(self.chatai, self.chatai_url)
        self.ui.menuType.setTitle(_translate("MainWindow", self.chatai))
        self.moveToChatAI()
        self.dataAcc.update_config('chatai', self.chatai)


    def show(self) -> None:
        super().show()
        self.open_first_page()
        self.activateWindow()

    def open_first_page(self):
        import os
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './html/index.html'))
        self.webEngineView.setUrl(QUrl.fromLocalFile(file_path))


    def check_chatai_logined(self):
        if self.chatai == 'chatGPT':
            self.webEngineView.page().runJavaScript(f"document.getElementById('prompt-textarea').outerHTML",
                                                                resultCallback=self.searchAI2)
        elif self.chatai == 'bard':
            self.webEngineView.page().runJavaScript(f"document.querySelector('rich-textarea').outerHTML",
                                                                resultCallback=self.searchAI2)
        elif self.chatai == 'clova-x':
            self.webEngineView.page().runJavaScript(f"document.getElementById('conversation-input').outerHTML",
                                                                resultCallback=self.searchAI2)


    def get_textinput_position(self):
        if self.chatai == 'chatGPT':
            return 120, 25
        elif self.chatai == 'bard':
            return 170, 60
        elif self.chatai == 'clova-x':
            return 170, 60

    def get_searchbutton_position(self):
        if self.chatai == 'chatGPT':
            return 50, 30
        elif self.chatai == 'bard':
            return 95, 60
        elif self.chatai == 'clova-x':
            return 95, 60

    def get_window_size(self):
        ratio = self.devicePixelRatio()
        if ratio == 0:
            ratio = 1
        w = self.width() * ratio
        h = self.height() * ratio
        return w, h

    def findInputLocation(self):
        x, y = self.get_textinput_position()
        w, h = self.get_window_size()
        clickX = self.x() + w - x
        clickY = self.y() + h - y
        pyautogui.moveTo(clickX, clickY)
        pyautogui.click()
        # print(f'Input location click x:{self.x()}, y:{self.y()}, width:{self.width()}, height:{self.height()}, clickX:{clickX}, clickY:{clickY}')


    def searchAi(self, data):
        print('searchAi!!')
        self.tempMousePosition = pyautogui.position()
        self.activateWindow()
        clipboard.copy(data)
        self.check_chatai_logined()

    def searchAI2(self, js_result):
        if not js_result:
            print('로그인이 필요합니다.')
            QMessageBox.information(self, 'Not logged on', 'Please Login first.')
            return
        self.findInputLocation()
        # time.sleep(1)
        self.delayHotKey(100, 'ctrl', 'v')
        self.delayKey(200, 'enter')
        # mouse position 원복
        pyautogui.moveTo(self.tempMousePosition)

    def delayHotKey(self, ms, key1, key2):
        print('delayHotKey ', key1, key2)
        setTimeout(pyautogui.hotkey, ms, key1, key2)

    def delayKey(self, ms, key):
        print('delayKey ', key)
        setTimeout(pyautogui.press, ms, key)

    def delayClick(self, clickX, clickY):
        print('delayClick ', clickX, clickY)
        pyautogui.moveTo(clickX + 1, clickY)
        pyautogui.click()

    def moveToChatAI(self):
        self.webEngineView.setUrl(QUrl(self.chatai_url))


    def loadFinished(self):
        print('loadFinished')
        print(self.webEngineView.url())
        # cookie = webview.page().profile()
        # if cookie is not None:

        #     print("results:", cookie.name(), cookie.value(), cookie.toRawForm())
