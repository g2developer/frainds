import sys
import os

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QApplication

from dataaccess import DataAccess
from voicerec import VoiceCommander
from windows import MainWindow

version = '1.0'


class MiniVoice:
    mainWindow = None
    qapp = None
    voiceCmdr = None
    dataAcc = None

    def __init__(self):
        print(f'frainds v{version}')
        # mini voice bot?
        # min vot?
        self.dataAcc = DataAccess()
        self.qapp = QApplication(sys.argv)
        self.mainWindow = MainWindow(self.dataAcc)
        self.mainWindow.show()

        # self.voiceCmdr = VoiceCommander()
        # self.voiceCmdr.sign_command.connect(self.command_handle)
        # self.voiceCmdr.sign_model_loaded.connect(self.mainWindow.moveToChatAI)
        # self.voiceCmdr.start()

    def command_handle(self, command_type, data):
        if command_type == 'exit':
            self.exit()
        elif command_type == 'search':
            self.mainWindow.searchAi(data)


    def exit(self):
        print('프로그램을 종료합니다.')
        if self.dataAcc:
            self.dataAcc.close()
        # sys.exit(self.exec())
        if self.voiceCmdr:
            self.voiceCmdr.stop()
        sys.exit()

    def exec(self):
        _exec = self.qapp.exec()
        print(f'_exec {_exec}')
        if self.voiceCmdr:
            self.voiceCmdr.stop()
        return _exec


if __name__ == "__main__":
    try:
        os.chdir(sys._MEIPASS)
        print(sys._MEIPASS)
    except:
        os.chdir(os.getcwd())

    app = MiniVoice()
    sys.exit(app.exec())
