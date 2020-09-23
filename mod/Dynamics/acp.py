import time
import numpy as np
from core import ESC
from mod.AroCore import AcpExecutor
from mod.Dynamics import Constraint
class IPE(AcpExecutor):
    def postProgress(self,datadict):
        joints=list()
        for aro in ESC.MAP_QUEUE[-1]:
            if type(aro)==Constraint:
                joints.append(aro)

        for joint in joints:
            if getattr(joint,'_master',True):
                joint._master=ESC.getAro(joint.master)
                joint._servant=ESC.getAro(joint.servant)
                joint._m_tar=ESC.getAro(joint.m_target)
                joint._s_tar=ESC.getAro(joint.s_target)
            master=joint._master
            servant=joint._servant
            m_tar=joint._m_tar
            s_tar=joint._s_tar
            pm=np.array(master.position)
            ps=np.array(servant.position)
            pj=np.array(m_tar.position)
            pt=np.array(s_tar.position)
            rm=pj-pm
            rs=pj-ps
            if getattr(joint,'_Im',True):
                if master.mass==np.inf:joint._Im=np.inf
                else:joint._Im=master.inertia[2]+master.mass*np.linalg.norm(rm)**2
                joint._Is=servant.inertia[2]+servant.mass*np.linalg.norm(rs)**2
            Im=joint._Im
            Is=joint._Is
            MIm=np.array([
                [rm[0]**2,-1*rm[0]*rm[1],0],
                [-1*rm[0]*rm[1],rm[1]**2,0],
                [0,0,1]])
            MIs=np.array([
                [rs[0]**2,-1*rs[0]*rs[1],0],
                [-1*rs[0]*rs[1],rs[1]**2,0],
                [0,0,1]])
            a=(1/master.mass+1/servant.mass)
            Mmass=np.linalg.inv(a*np.identity(3)
                +1/Im*MIm
                +1/Is*MIs)
            bias=-0.2/ESC.TIME_STEP*(pt-pj)

            i=0
            IT=5
            ERR=1e-4
            p=[1,1,1]
            while(i<IT and (abs(p[0])>ERR or abs(p[1])>ERR)):
                vm=np.array(getattr(master,'velocity',[0,0,0]))
                vs=np.array(getattr(servant,'velocity',[0,0,0]))
                wm=np.array(getattr(master,'agl_v',[0,0,0]))
                ws=np.array(getattr(servant,'agl_v',[0,0,0]))
                dv=vm+np.cross(wm,rm)-vs-np.cross(ws,rs)
                p=np.dot(Mmass,(dv+bias))
                fp=p/ESC.TIME_STEP
                master.velocity-=fp/master.mass*ESC.TIME_STEP
                servant.velocity+=fp/servant.mass*ESC.TIME_STEP
                master.agl_v-=np.cross(rm,fp)/Im*ESC.TIME_STEP
                servant.agl_v+=np.cross(rs,fp)/Is*ESC.TIME_STEP
                i+=1

            ESC.setAro(master.AroID,{'velocity':master.velocity.tolist(),'agl_v':master.agl_v.tolist()})
            ESC.setAro(servant.AroID,{'velocity':servant.velocity.tolist(),'agl_v':servant.agl_v.tolist()})
        return {}
    pass
