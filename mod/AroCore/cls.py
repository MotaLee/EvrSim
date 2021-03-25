from core import estl
class ModComVar(object):
    def __init__(self,mgd:dict) -> None:
        self.mod_name=mgd['MOD_NAME']
        self.mod_ver=mgd['MOD_VER']
        self.idx_aro=mgd['ARO_INDEX']
        self.idx_acp=mgd['ACP_INDEX']
        self.idx_mdl=mgd['MODEL_INDEX']
        self.idx_tool=dict()
        self.bindTool(mgd)
        return

    def bindTool(self,mgd:dict):
        for k,v in mgd.items():
            if isinstance(v,estl.ToolBase):
                self.idx_tool[k]=v
        return

    def getTool(self,name):
        out:estl.ToolBase=self.idx_tool[name]
        return out
    pass
