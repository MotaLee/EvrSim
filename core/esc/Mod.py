import mod
from core import esc as ESC
def loadMod(modlist,unload=False):
    ''' Lv1: Load Mod from MOD_LIST.
        Include models and setting.
        * Para unload: unload mod form ESC which not in para modlist.'''
    for modname in modlist:
        if modname not in ESC.MOD_TREE_DICT:
            exec('import mod.'+modname)
            ESC.MOD_TREE_DICT[modname]=ModTree(modname)

        mod_setting=eval('mod.'+modname+'.MOD_PERF')
        ESC.setSim(mod_setting,usercall=False)

        model_index=eval('mod.'+modname+'.MODEL_INDEX')
        for model in model_index:
            ESC.loadModelFile((modname,model))
    if unload:
        for modname in ESC.MOD_TREE_DICT:
            'todo: unload mods'
    return

def getModAttr(modname,attrname=None):
    ''' Return attribute in mod or mod self.
        * Para attrname: default for mod self.'''
    if attrname is None:
        try:ret=eval('mod.'+modname)
        except BaseException as e:ESC.err(e)
    else:
        try:ret=eval('mod.'+modname+'.'+attrname)
        except BaseException as e:ESC.err(e)
    return ret

class ModTree(ESC.EsTree):
    def __init__(self,modname):
        super().__init__()
        modptr=getModAttr(modname)
        root=self.appendNode(None,self.NodeClass(
            label=modptr.MOD_NAME,data=modptr.MOD_VER))
        self.node_perf=self.appendNode(root,self.NodeClass(
            label='Perference',data=modptr.MOD_PERF))
        self.node_aro=self.appendNode(root,self.NodeClass(
            label='Aro',data=modptr.ARO_INDEX))
        self.node_acp=self.appendNode(root,self.NodeClass(
            label='Acp',data=modptr.ACP_INDEX))
        self.node_mdl=self.appendNode(root,self.NodeClass(
            label='Model',data=modptr.MODEL_INDEX))

        for aro in self.node_aro.data:
            self.appendNode(self.node_aro,self.NodeClass(label=aro))
        for acp in self.node_acp.data:
            self.appendNode(self.node_acp,self.NodeClass(label=acp))
        for mdl in self.node_mdl.data:
            self.appendNode(self.node_mdl,self.NodeClass(label=mdl))

        return

    pass
