import os
import sys

from PyQt6.QtWidgets import QApplication

from actions.websearch import WebSearch
from command import Command
from dataaccess import DataAccess
from utils import has
from voicerec import VoiceRecognition
from windows import MainWindow

__version__ = '0.1'


class Frainds:
    language = 'en'
    _name = 'frainds'
    qapp = None
    mainWindow = None

    dataAcc = None

    voiceRec = None
    voiceTextWin = None

    command = None

    websearch = WebSearch()

    # ai와 chatting 중인지?
    keep_goning_chat = False

    def __init__(self):
        print(f'frainds v{__version__}')
        # mini voice bot?
        # min vot?
        self.dataAcc = DataAccess()
        self.language = self.dataAcc.get_config_value('language')
        self._name = self.dataAcc.get_config_value('_name')

        self.qapp = QApplication(sys.argv)
        self.mainWindow = MainWindow(self.dataAcc)
        self.mainWindow.show()
        self.mainWindow.ui.actionVoice_recognition.triggered.connect(self.toggle_voice_rec)
        config_mic = self.dataAcc.get_config_value('mic')
        self.mainWindow.ui.actionVoice_recognition.setChecked(config_mic == 'on')
        self.mainWindow.ui.actionkeep_going_chat.triggered.connect(self.set_keep_goning_chat)
        self.mainWindow.ui.checkBox.stateChanged.connect(self.set_keep_goning_chat)
        self.mainWindow.ui.actionExit.triggered.connect(self.exit)

        self.command = Command(self.dataAcc)

        self.voiceRec = VoiceRecognition(config_mic == 'on')
        self.voiceRec.sign_listen.connect(self.listen_handle)
        self.voiceRec.sign_model_loaded.connect(self.mainWindow.moveToChatAI)


    def toggle_voice_rec(self, flag):
        print('toggle_voice_rec :', flag)
        if not flag:
            self.voiceRec.stop()
        else:
            if not self.voiceRec.recording:
                self.voiceRec.start()
        self.dataAcc.update_config('mic', 'on' if flag else 'off')


    def set_keep_goning_chat(self, flag):
        self.keep_goning_chat = flag
        self.mainWindow.ui.actionkeep_going_chat.setChecked(flag)
        self.mainWindow.ui.checkBox.setChecked(flag)

    def listen_handle(self, txt):
        cmm_type, data = self.command.find_command(txt)
        print('커맨드 타입:', cmm_type)
        if not cmm_type:
            if self.keep_goning_chat:
                self.mainWindow.searchAi(data)
            return
        if cmm_type == 'exit':
            self.exit()
        elif has(cmm_type, 'call_me'):
            self.mainWindow.activateWindow()
        elif has(cmm_type, 'chat_ai'):
            if has(cmm_type, ['off', 'stop']):
                self.set_keep_goning_chat(False)
            elif has(cmm_type, ['on', 'start']):
                self.set_keep_goning_chat(True)
            else:
                # self.set_keep_goning_chat(True)
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
