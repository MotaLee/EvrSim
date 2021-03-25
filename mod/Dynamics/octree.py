# import os,sys
import interval
import numpy as np
from core import ESC,esgl
GLC=esgl.glc
class OcTree(ESC.EsTree):
    def __init__(self):
        self.bound=100
        root=OcTreeNode([0])
        super().__init__(root)
        return

    def buildTree(self,rebuild=False):
        if rebuild:self.__init__()
        alladp=GLC.getAllAdp()
        for adp in alladp:
            v=getattr(adp.Aro,'velocity',[0,0,0])
            if id(adp) not in self.tree or np.linalg.norm(v,ord=1)!=0:
                aabb=esgl.getAABB(adp)
                setted=False
                p=[0,0,0]
                while setted:
                    pass
                    # if()
                node=OcTreeNode()
                # parent=
                # self.appendNode(node,parent)
        return

    def getColPairs(self,tars=list()):
        pairs=list()
        TOR=1e-4
        if len(tars)==0:tars=GLC.getAllAdp()
        for adp1 in tars:
            aabb1=esgl.getAABB(adp1)
            xi=interval.Interval(aabb1[0]+TOR,aabb1[1]-TOR)
            yi=interval.Interval(aabb1[2]+TOR,aabb1[3]-TOR)
            zi=interval.Interval(aabb1[4]+TOR,aabb1[5]-TOR)
            for adp2 in tars:
                if adp1==adp2:continue
                if (adp2,adp1) in pairs:continue
                aabb2=esgl.getAABB(adp2)
                xj=interval.Interval(aabb2[0]+TOR,aabb2[1]-TOR)
                yj=interval.Interval(aabb2[2]+TOR,aabb2[3]-TOR)
                zj=interval.Interval(aabb2[4]+TOR,aabb2[5]-TOR)
                if xi.overlaps(xj) and yi.overlaps(yj) and zi.overlaps(zj):
                    pairs.append((adp1,adp2))
        return pairs
    pass

class OcTreeNode(ESC.TreeNode):
    def __init__(self,block,ntype='space'):
        super().__init__()
        self.type=ntype   # Emum for space/axis;
        self.block=block    # A list sequence of subspace number;

        self.items=list()
        return
    pass
