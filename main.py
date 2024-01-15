import sys
import os
import threading
import time

import pyautogui
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QApplication

from actions.websearch import WebSearch
from command import Command
from dataaccess import DataAccess
from utils import has
from voicerec import VoiceRecognition
from windows import MainWindow

version = '1.0'


class Frainds:
    language = 'en'
    qapp = None
    mainWindow = None

    dataAcc = None

    voiceRec = None
    voiceTextWin = None

    command = None

    websearch = WebSearch()

    # ai와 chatting 중인지?
    is_ai_chatting = False

    def __init__(self):
        print(f'frainds v{version}')
        # mini voice bot?
        # min vot?
        self.dataAcc = DataAccess()
        self.language = self.dataAcc.get_config_value('language')

        self.qapp = QApplication(sys.argv)
        self.mainWindow = MainWindow(self.dataAcc)
        self.mainWindow.show()
        self.mainWindow.ui.actionVoice_recognition.triggered.connect(self.toggle_voice_rec)
        config_mic = self.dataAcc.get_config_value('mic')
        self.mainWindow.ui.actionVoice_recognition.setChecked(config_mic == 'on')

        self.command = Command(self.dataAcc)

        self.voiceRec = VoiceRecognition()
        self.voiceRec.sign_listen.connect(self.listen_handle)
        self.voiceRec.sign_model_loaded.connect(self.mainWindow.moveToChatAI)
        if config_mic == 'on':
            self.voiceRec.start()

    def toggle_voice_rec(self, flag):
        print('toggle_voice_rec :', flag)
        if not flag:
            self.voiceRec.stop()
        else:
            if not self.voiceRec.recording:
                self.voiceRec.start()
        self.dataAcc.update_config('mic', 'on' if flag else 'off')


    def listen_handle(self, txt):
        cmm_type, data = self.command.find_command(txt)
        print('커맨드 타입:', cmm_type)
        if not cmm_type:
            if self.is_ai_chatting:
                self.mainWindow.searchAi(data)
            return
        if cmm_type == 'exit':
            self.exit()
        elif has(cmm_type, 'chat_ai'):
            if has(cmm_type, ['off', 'stop']):
                self.is_ai_chatting = False
            else:
                self.is_ai_chatting = True
                self.mainWindow.searchAi(data)
        elif cmm_type == 'search_web':
            self.websearch.action(data)
        elif cmm_type == 'off_mic':
            self.mainWindow.ui.actionVoice_recognition.setChecked(False)
            self.toggle_voice_rec(False)

    def exit(self):
        print('프로그램을 종료합니다.')
        if self.dataAcc:
            self.dataAcc.close()
        # sys.exit(self.exec())
        if self.voiceRec:
            self.voiceRec.stop()
        sys.exit()

    def exec(self):
        _exec = self.qapp.exec()
        print(f'프로그램을 종료합니다 {_exec}')
        if self.dataAcc:
            self.dataAcc.close()
        if self.voiceRec:
            self.voiceRec.stop()
        return _exec


if __name__ == "__main__":
    try:
        os.chdir(sys._MEIPASS)
        print(sys._MEIPASS)
    except:
        os.chdir(os.getcwd())

    app = Frainds()
    sys.exit(app.exec())
