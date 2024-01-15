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

        for tg in tg_lst:
            if has(txt, tg[1].split(',')):
                cmm_target = tg[0]

        if cmm_type == 'search' and not cmm_target:
            cmm_target = 'chat_ai'
        # print('cmm_type, cmm_target ', cmm_type, cmm_target)
        if not cmm_type:
            return cmm_type, txt
        if not cmm_target and cmm_type:
            return cmm_type, txt
        return cmm_type+'_'+cmm_target, txt


if __name__ == "__main__":
    import sys
    dataAcc = DataAccess()
    cmm = Command(dataAcc)
    cmmtype, txt = cmm.find_command('구글에서 파이썬으로 프로그램만드는 법 좀 찾아줘')
    print(cmmtype, txt)
