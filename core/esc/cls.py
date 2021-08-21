# Class;
import multiprocessing as mp
from multiprocessing.queues import Queue
class TreeNode(object):
    def __init__(self,**argkw):
        ''' Para argkw: nid/label/parent/children/depth/data'''
        self.nid=argkw.get('nid',0)
        self.label=argkw.get('label','Node')
        self.children=argkw.get('children',list())
        self.parent=argkw.get('parent',None)
        self.data=argkw.get('data',None)
        self.depth=argkw.get('depth',0)
        return
    pass
class EsTree(object):
    def __init__(self,**argkw):
        ''' Para argkw: tree/.'''
        self.tree=dict()
        self.linkdict_parent=dict()
        self.linkdict_children=dict()
        self.max_id=-1
        self.NodeClass=TreeNode
        self.root=None

        self.loadTree(argkw.get('tree',{}))
        return

    def loadTree(self,tree):
        if len(tree)==0:return
        if isinstance(tree,str):tree=eval(tree)
        for k,v in tree.items():
            k=int(k)
            node=self.NodeClass(**v)
            self.tree[k]=node
            self.linkdict_parent[k]=v['parent']
            if v['parent'] is None:self.root=node
            self.linkdict_children[k]=v['children']
        self.max_id=max([self.max_id]+list(self.tree.keys()))
        return

    def saveTree(self,savedata=False):
        ''' Return tree dict string without data attr.
            Para savedata: problem may occur if data attr too complex.'''
        dict_out=dict()
        for k,v in self.tree.items():
            tmp=dict(v.__dict__)
            if not savedata:del tmp['data']
            dict_out[k]=tmp
        # dict_out=json.dumps(dict_out,indent=4,ensure_ascii=False)
        # dict_out=str(dict_out).replace('null','None')
        return str(dict_out)

    def getNode(self,index):
        'Return None if not found.'
        if isinstance(index,int):
            return self.tree[index]
        elif isinstance(index,str):
            for node in self.tree.values():
                if node.label==index:return node
        return None

    def appendNode(self,parent,node:TreeNode):
        ''' Append a node under the giving parent.
            * Para node: Accept TreeNode,
                The node's nid/parent/chidren/depth needn't to be set.
            * Para parent: Accept nid/label/TreeNode/None.'''
        from core.esc import ESC as ESC
        self.max_id+=1
        node.nid=self.max_id
        if parent is not None:
            if not isinstance(parent,self.NodeClass):
                parent=self.getNode(parent)
            if parent is None:ESC.err('Parent node not found.')
            self.linkdict_parent[node.nid]=parent.nid
            if parent.nid not in self.linkdict_children:
                self.linkdict_children[parent.nid]=list()
            self.linkdict_children[parent.nid].append(node.nid)
            node.parent=parent.nid
            node.depth=parent.depth+1
            parent.children.append(node.nid)
        else:
            self.linkdict_parent[node.nid]=None
            self.root=node
        self.tree[node.nid]=node
        return node

    def delNode(self,node):
        ''' Delete a node and its subtree.
            * Para node: Accept nid/label/TreeNode.'''
        from core.esc import ESC as ESC
        if not isinstance(node,self.NodeClass):
            node=self.getNode(node)
        if node is None:return ESC.err('Node not found.')
        pnid=self.linkdict_parent[node.nid]
        if pnid is not None:
            self.tree[pnid].children.remove(node)
            self.linkdict_children[pnid].remove(node.nid)
        else:self.__init__(None)
        subtree=self.travsalTree(node,lambda e: None)
        for nid in subtree:
            del self.tree[nid]
            del self.linkdict_parent[nid]
            del self.linkdict_children[nid]
        return

    def travsalTree(self,start=None,method=None,reverse=False):
        'Travsal tree using giving method and return travsal track.'
        if start is None: start=self.root
        if method is None:method=self.visitNode
        stack=[start]
        visited=list()
        track=list()
        while(len(stack)!=0):
            node=stack[-1]
            if node.nid in visited:
                stack.pop()
                track.append(node.nid)
                continue
            children_ready=True
            if self.linkdict_children[node.nid] is not None:
                for child in self.linkdict_children[node.nid]:
                    if child not in visited:
                        stack.append(self.tree[child])
                        children_ready=False
                        break
            if children_ready:
                visited.append(node.nid)
                method(node)
        if reverse:track=list(reversed(track))
        return track

    def visitNode(self,node):
        ''' Overrided.'''
        return

    def clearTree(self):
        self.__init__()
        return
    pass

class EsMesh(object):
    'todo'
    pass

class EsQueue(Queue):
    def __init__(self):
        super().__init__(ctx=mp.get_context())
        return
    pass
class EsProcess(mp.Process):
    def __init__(self,**argkw):
        ''' EvrSim running process.
            * Para argkw: stdin/stdout;'''
        self.stdin=EsQueue()
        self.stdout=EsQueue()
        self.flag_exit=False
        super().__init__(target=self.running, daemon=True)
        return

    def running(self):
        ''' Empty.'''
        return

    def send(self,msg:str):
        try:
            self.stdin.put(msg)
            out=True
        except BaseException:out=False
        return out

    def recv(self):
        try:
            out=self.stdout.get(timeout=0.1)
        except TimeoutError:out=None
        return out
    pass

class EsEnum(object):
    def __init__(self,items:list,current=None,prev=None):
        ''' * Para items: Set of enum;
            * Para currnt: Inital item, None default for select the 1st item as current;
            * Para prev: Inital previous item, None default for the same with current;
            '''
        self.items=items
        if current is None:
            self.current=self.items[0]
        else:self.set(current)
        if prev is None:
            self.prev=self.current
        else:self.prev=prev
        return

    def set(self,item):
        if item in self.items:
            self.prev=self.current
            self.current=item
        return

    def get(self):return self.current

    def getPrev(self):return self.prev
    def rollback(self):self.current=self.prev

    def val(self,item):return item==self.current
    pass
class SimTree(EsTree):
    def __init__(self,tree):
        super().__init__(tree=tree)
        self.node_perf=self.getNode('Perference')
        self.node_map=self.getNode('Map')
        self.node_model=self.getNode('Model')
        self.node_mod=self.getNode('Mod')
        return
    pass

class ModTree(EsTree):
    def __init__(self,modname):
        super().__init__()
        from core.esc import ESC as ESC
        modptr=ESC.getModAttr(modname)
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
