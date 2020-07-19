from mod.AroCore import Acp
class InstanceCenter(Acp):
    ''' Calculate the instance center of a rigid body.

        Addition: None.

        Outport: output vec3.

        Inport: input RigidGroup;'''
    def __init__(self):
        super().__init__()
        self.inport={1:None}
        self.outport={1:None,2:list()}
        self.port={1:'in',2:'out'}
        return

    def AcpProgress(self,datadict):
        rgdict=datadict[self.inport[1]]

        return
    pass
