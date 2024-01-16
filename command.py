import os
from sys import platform

from dataaccess import DataAccess
from utils import has


class Command:
    dataAcc = None
    ai_chatting = False

    def __init__(self, dataAcc: DataAccess):
        self.dataAcc = dataAcc


    def find_command(self, txt):
        cmm_type = None
        cmm_target = None
        cmm_lst = self.dataAcc.cmm_lst
        tg_lst = self.dataAcc.cmm_target_lst

        for cmm in cmm_lst:
            if has(txt, cmm[1].split(',')):
                cmm_type = cmm[0]
                break

        for tg in tg_lst:
            if has(txt, tg[1].split(',')):
                cmm_target = tg[0]
                break

        print(cmm_type, cmm_target)

        if cmm_type == 'open' and cmm_target == 'filebrowser':
            self.open_filebrowser()

        if cmm_type == 'open' and cmm_target == 'downfolder':
            self.open_filebrowser(cmm_target)

        if cmm_type == 'search' and not cmm_target:
            cmm_target = 'chat_ai'
        # print('cmm_type, cmm_target ', cmm_type, cmm_target)
        if not cmm_type:
            return cmm_type, txt
        if not cmm_target and cmm_type:
            return cmm_type, txt
        return cmm_type+'_'+cmm_target, txt

    def open_filebrowser(self, open_target=None):
        my_path = ''
        if platform.system() == 'Windows':
            my_path = '::{20D04FE0-3AEA-1069-A2D8-08002B30309D}'
        else :
            my_path = os.path.expanduser('~/')

        if open_target == 'downfolder':
            my_path = os.path.expanduser('~/Downloads')
        os.startfile(my_path)


if __name__ == "__main__":
    # dataAcc = DataAccess()
    # cmm = Command(dataAcc)
    # cmmtype, txt = cmm.find_command('구글에서 파이썬으로 프로그램만드는 법 좀 찾아줘')
    # print(cmmtype, txt)

    my_path = os.path.expanduser('~/Downloads')
    os.startfile(os.path.expanduser('~/'))
    # lst = '다운로드폴더,다운로드 폴더,download foler,download directory,다운폴더'
    # print(has('다운로드 폴더 열어줘', lst.split(','), True))
