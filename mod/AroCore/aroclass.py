from core import ESC
# Aro class defination;
class Aro(object):
    def __init__(self):
        self.AroID=0
        cn=str(type(self))
        self.AroClass=cn[8:cn.find('>')-1]
        self.parent=None

        self.AroName=''
        self.desc=''
        return
    pass

class AroSpace(Aro):
    '''Addition Arove: space_set;'''
    def __init__(self):
        super().__init__()
        self.space_list=list()
        return
    pass
