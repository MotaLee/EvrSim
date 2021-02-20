import numpy as np
import _glm as glm
from interval import Interval as Itv
from core import ESC,esgl
from mod.AroCore import AcpExecutor
from mod.Dynamics import Constraint,OcTree,ForceField,RigidBody,PointForce
class IPE(AcpExecutor):
    def postProgress(self,datadict):
        joints=list()
        for aro in ESC.MAP_QUEUE[0].values():
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
            bias=-0.2/ESC.len_timestep*(pt-pj)

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
                fp=p/ESC.len_timestep
                master.velocity-=fp/master.mass*ESC.len_timestep
                servant.velocity+=fp/servant.mass*ESC.len_timestep
                master.agl_v-=np.cross(rm,fp)/Im*ESC.len_timestep
                servant.agl_v+=np.cross(rs,fp)/Is*ESC.len_timestep
                i+=1

            ESC.setAro(master.AroID,{'velocity':master.velocity.tolist(),'agl_v':master.agl_v.tolist()})
            ESC.setAro(servant.AroID,{'velocity':servant.velocity.tolist(),'agl_v':servant.agl_v.tolist()})
        return {}
    pass

class CPE(AcpExecutor):
    def __init__(self):
        super().__init__()
        self._octree=OcTree()
        self.EPSILON=1e-4
        return

    def postProgress(self,datadict):
        pairs=self._octree.getColPairs()
        colibodys=set()
        colidata=list()
        for pair in pairs:
            aro0=ESC.getAro(pair[0].name)
            aro1=ESC.getAro(pair[1].name)
            if aro1==aro0:continue
            if not (isinstance(aro0,RigidBody) and isinstance(aro1,RigidBody)):continue
            is_coll,simplex=self.gjk(pair)
            if is_coll:
                v_tgh,d_tgh=self.epa(pair,simplex)
                if d_tgh>self.EPSILON:
                    p_coli=self.getColiPos(pair,d_tgh)
                    colibodys.add(aro0)
                    colibodys.add(aro1)
                    colidata.append((aro0,aro1,v_tgh,d_tgh,p_coli))

        self._bodys,self._forces,self._fields=list(),list(),list()
        for aro in ESC.getFullMap():
            if isinstance(aro,RigidBody):self._bodys.append(aro)
            elif isinstance(aro,PointForce):self._forces.append(aro)
            elif isinstance(aro,ForceField):self._fields.append(aro)
        for coll in colidata:
            arovea,aroveb=self.collUpdate(coll)
            ESC.setAro(coll[0],arovea)
            ESC.setAro(coll[1],aroveb)

        for body in self._bodys:
            if body.mass!=np.inf and body.mass!=0:
                ESC.setAro(body,self.bodyMotion(body))
        return

    def bodyMotion(self,body):
        if body.mass==0 or body.mass==np.inf:return {}
        'todo: inertia'
        Ita=[body.mass/6]*3
        position=(np.array(body.position)+np.array(body.velocity)/esgl.FPS).tolist()
        v_aglv=glm.vec3(body.agl_v)
        if glm.l1Norm(v_aglv)!=0:
            rmat=glm.rotate(glm.mat4(1.0),glm.l2Norm(v_aglv)/esgl.FPS,v_aglv)
            x2=rmat*glm.vec4(body.LCS[0]+[1.0])
            y2=rmat*glm.vec4(body.LCS[1]+[1.0])
            z2=rmat*glm.vec4(body.LCS[2]+[1.0])
            LCS=[list(x2)[0:3],list(y2)[0:3],list(z2)[0:3]]
            # print(y2)
        else:LCS=body.LCS
        velocity=(np.array(body.velocity)+np.array(body.force)/body.mass/esgl.FPS).tolist()
        agl_v=np.array(body.agl_v)
        moment=np.array([0,0,0])
        dI=np.array([
            (Ita[1]-Ita[2])*agl_v[1]*agl_v[2],
            (Ita[2]-Ita[0])*agl_v[2]*agl_v[0],
            (Ita[0]-Ita[1])*agl_v[0]*agl_v[1]])
        agl_acc=(dI+moment)/Ita
        agl_v=(agl_v+agl_acc/esgl.FPS).tolist()
        force=np.array([0,0,0])
        for force in self._forces:
            if force.target==body.AroID:
                force+=np.array(force.value)
                moment+=np.cross(np.array(force.value),np.array(force.position))
        for field in self._fields:
            if field.shape is None:
                force+=np.array(field.function)
        force=force.tolist()
        moment=moment.tolist()
        bodydict={
            'inertia':Ita,'position':position,
            'agl_v':agl_v,'LCS':LCS,'velocity':velocity,
            'force':force,'moment':moment}
        return bodydict

    def epa(self,pair,simplex):
        if len(simplex)==2:
            vn=np.cross(np.array([0,1,0]),simplex[0]-simplex[1])
            if np.linalg.norm(vn)<self.EPSILON:
                vn=np.cross(np.array([0,0,1]),simplex[0]-simplex[1])
            p3=self.supportMD(pair,vn)
            p4=self.supportMD(pair,-vn)
            for p in simplex:
                if (p3==p).all() or (p4==p).all():
                    return [0,0,0],0
            simplex=np.row_stack((simplex,p3))
            simplex=np.row_stack((simplex,p4))
        elif len(simplex)==3:
            vn=np.cross(simplex[2]-simplex[0],simplex[0]-simplex[1])
            p4=self.supportMD(pair,vn)
            p5=self.supportMD(pair,-vn)
            p4in=False
            p5in=False
            for p in simplex:
                if (p4==p).all():
                    p4in=True
                    break
                if (p5==p).all():
                    p5in=True
                    break
            if not p4in:simplex=np.row_stack((simplex,p4))
            elif not p5in:simplex=np.row_stack((simplex,p5))
            else:return [0,0,0],0

        s2=-np.inf
        s1=np.inf
        v_though=np.array([0,0,0])
        face_index=[(0,1,2),(1,2,3),(0,2,3),(0,1,3)]
        fn=(0,0,0)
        d_dict=dict()
        imax=len(pair[0].VA)*len(pair[1].VA)
        while imax>0:
            for face in face_index:
                if face not in d_dict:
                    dis,vn=esgl.getDisFormPtToPlane(
                        np.array([0,0,0]),[
                            simplex[face[0]],
                            simplex[face[1]],
                            simplex[face[2]]],vn=True)
                    d_dict[face]=(dis,vn)
                dis=d_dict[face][0]
                vn=d_dict[face][1]
                if dis==0:
                    fn=face
                    for ip in range(0,len(simplex)):
                        if ip not in face:
                            res=np.dot(simplex[face[0]]-simplex[ip],vn)
                            if res!=0:
                                v_though=np.sign(res)*vn
                                break
                    break
                elif dis<s1:
                    fn=face
                    s1=dis
                    if np.dot(simplex[fn[0]],vn)<0:v_though=-vn
                    else:v_though=vn

            p_new=self.supportMD(pair,v_though)
            s2=np.dot(p_new,v_though)
            if abs(s2-s1)>self.EPSILON:
                for p in simplex:
                    if (p_new==p).all():return v_though,s1
                s1=np.inf
                del d_dict[fn]
                ip=len(simplex)
                face_index.remove(fn)
                face_index+=[(ip,fn[0],fn[1]),(ip,fn[0],fn[2]),(ip,fn[1],fn[2])]
                simplex=np.row_stack((simplex,p_new))
            else:break
            imax-=1
        return v_though,s2

    def gjk(self,pair):
        # // center difference as initial direction
        pa=np.array(pair[0].Aro.position)
        pb=np.array(pair[1].Aro.position)
        direct=-np.array(pa-pb)
        direct=direct/np.linalg.norm(direct)
        if np.linalg.norm(direct)<0.001:direct = np.array([1,0,0])
        # // init
        simplex_point = self.supportMD(pair, direct)
        simplex=np.array([simplex_point.tolist()],dtype=np.float32)
        direct = -simplex_point
        # // main loop
        max_iteration = max(len(pair[0].VA), len(pair[1].VA))
        while max_iteration>0:
            simplex_point = self.supportMD(pair, direct)
            if np.dot(simplex_point,direct)<0:return False,None
            simplex=np.row_stack((simplex,simplex_point))
            res,simplex,direct=self.simplexOrigin(simplex, direct)
            if res:return True,simplex
            elif np.linalg.norm(direct)<self.EPSILON:return False,None
            max_iteration-=1
        return False,None

    def getColiPos(self,pair,depth=0):
        a=pair[0]
        b=pair[1]
        area_a=list()
        area_b=list()
        vN0=0
        for f in b.EA:
            pA=esgl.getTransPosition(b.VA[f[0]],b.trans)
            pB=esgl.getTransPosition(b.VA[f[1]],b.trans)
            pC=esgl.getTransPosition(b.VA[f[2]],b.trans)
            vN=np.cross(pB-pA,pC-pA)
            vN/=np.linalg.norm(vN)
            sat=esgl.getSAT([pA,pB,pC])
            if len(area_b)==0:
                for p in a.VA:
                    pO=esgl.getTransPosition(p,a.trans)
                    condi=True
                    for i in range(0,3):
                        condi&=pO[i]>sat[2*i]-self.EPSILON-depth
                        condi&=pO[i]<sat[2*i+1]+self.EPSILON+depth
                    if condi:
                        area_a.append(pO)
                        vN0=vN
                        if len(area_b)==0:area_b+=[pA,pB,pC]
            else:
                c3=abs(np.dot(vN,vN0)-1)<depth+self.EPSILON
                if c3:area_b+=[pA,pB,pC]
        la=len(area_a)
        if la==0:
            'todo:edge to edge'
            area=self.getColiPos((b,a),depth)
        elif la==1:area=area_a[0]
        # elif la==2:pass
        else:
            'todo: more precise collision point'
            sata=esgl.getSAT(area_a)
            satb=esgl.getSAT(area_b)
            area=np.array([0,0,0])
            for i in range(0,3):
                axis=[sata[2*i],sata[2*i+1],satb[2*i],satb[2*i+1]]
                axis.remove(max(axis))
                axis.remove(min(axis))
                area[i]=(axis[0]+axis[1])/2
        return area

    def simplexOrigin(self,s,d):
        contain_origin = False
        slen=len(s)
        if slen==2:
            contain_origin,s,d = self.simplex2(s, d)
        elif slen==3:
            contain_origin,s,d= self.simplex3(s, d)
        elif slen==4:
            contain_origin,s,d =self.simplex4(s, d)
        return contain_origin,s,d

    def simplex4(self,s,d):
        A=s[3]
        B=s[2]
        C=s[1]
        D=s[0]

        AO=-A
        AB=B-A
        AC=C-A
        AD=D-A

        ABC = np.cross(AB,AC)    # // normal to ABC
        ACD = np.cross(AC,AD)    # // normal to ACD
        ADB = np.cross(AD,AB)   # // normal to ADB

        AD_ABC =np.dot(ABC,AD)   # // AD project on normal of ABC
        AB_ACD =np.dot(ACD,AB)   # // AB project on normal of ACD
        AC_ADB =np.dot(ADB,AC)  # // AC project on normal of ADB

        AO_ABC =np.dot(ABC,AO)  # // AO project on normal of ABC
        AO_ACD =np.dot(ACD,AO)   # // AO project on normal of ACD
        AO_ADB =np.dot(ADB,AO)   # // AO project on normal of ADB

        inside_ABC = AD_ABC * AO_ABC > self.EPSILON
        inside_ACD = AB_ACD * AO_ACD > self.EPSILON
        inside_ADB = AC_ADB * AO_ADB > self.EPSILON

        if inside_ABC and inside_ACD and inside_ADB:
            # // origin inside tetrahedron
            return True,s,d
        elif not inside_ABC:
            # // origin outside ABC
            # // remove D
            s[0] = s[1]
            s[1] = s[2]
            s[2] = s[3]
            s=s[:-1]
        elif not inside_ACD:
            # // origin outside ACD
            # // remove B
            s[2] = s[3]
            s=s[:-1]
        else:
            # // origin outside ADB
            # // remove C
            s[1] = s[2]
            s[2] = s[3]
            s=s[:-1]
        return self.simplex3(s,d)

    def simplex3(self,s,d):
        A = s[2]
        B = s[1]
        C = s[0]
        AB = B - A
        AC = C - A
        AO =- A
        ABC = np.cross(AB,AC)
        ACBB =np.cross(np.cross(AC,AB),AB)  # AC.cross(AB).cross(AB); // norm to AB toward far from C
        ABCC =np.cross(np.cross(AB,AC),AC)  # AB.cross(AC).cross(AC); // norm to AC toward far from B

        if np.dot(ACBB,AO)> self.EPSILON:
            # // origin lies on outside of AB
            d = ACBB
            return False,s,d

        if np.dot(ABCC,AO) > self.EPSILON:
            #  // origin lies on outside of AC
            d = ABCC
            return False,s,d

        dot =np.dot(ABC,AO)
        # // origin lies in ABC region
        if dot > self.EPSILON:
            d = ABC
            return False,s,d
        elif dot < self.EPSILON:
            d = -ABC
            return False,s,d
        else:
            # // origin lies in ABC triangle
            return True,s,d
        return

    def simplex2(self,s,d):
        A = s[1]
        B = s[0]
        AB = B - A
        AO =-A
        ABOO = np.cross(np.cross(AB,AO),AO)  # // norm to AB toward origin
        if np.linalg.norm(ABOO) <= self.EPSILON:  # // origin lies on
            return True,s,d
        else:
            d = ABOO
            return False,s,d
        return

    def supportMD(self,pair,direct):
        a = self.getSupport(pair[0],direct)
        b = self.getSupport(pair[1],-direct)
        return a - b

    def getSupport(self,adp,direct):
        ld=np.linalg.norm(direct)
        if ld==0:raise BaseException()
        # print(ld)
        p=esgl.getTransPosition(adp.VA[0],adp.trans)
        maxp=p
        maxpl=np.dot(maxp,direct)/ld
        for p_va in adp.VA:
            p=esgl.getTransPosition(p_va,adp.trans)
            length=np.dot(p,direct)/ld
            if length>=maxpl:
                maxp=p
                maxpl=length
        return maxp

    def collUpdate(self,colldata):
        kBiasFactor = 0.2    # // 弹性碰撞系数
        a=colldata[0]
        b=colldata[1]
        v_tgh = colldata[2]  # // 接触面
        d_tgh=colldata[3]
        p_coll=colldata[4]
        ve_tgh=v_tgh/np.linalg.norm(v_tgh)
        ra=p_coll-np.array(a.position,dtype=np.float64)
        rb=p_coll-np.array(b.position,dtype=np.float64)

        vea_tgh=-1*np.sign(np.dot(ve_tgh,rb-ra))*ve_tgh
        veb_tgh=-1*vea_tgh
        voa=np.array(a.velocity,dtype=np.float64)
        vob=np.array(b.velocity,dtype=np.float64)
        woa=np.array(a.agl_v,dtype=np.float64)
        wob=np.array(b.agl_v,dtype=np.float64)
        va=voa+np.cross(woa,ra)
        vb=vob+np.cross(wob,rb)
        dv=vb-va
        dv_x=np.dot(dv,veb_tgh)*veb_tgh/np.linalg.norm(dv)
        # dv_y=dv-dv_x
        # dv_desire=dv_y-kBiasFactor*dv_x
        if a.mass==np.inf:
            wea=np.array([0,0,0])
            vea=np.array([0,0,0])
        else:
            wea=np.dot(np.linalg.inv(np.diag(a.inertia)),np.cross(-vea_tgh,ra))
            vea=vea_tgh/a.mass+np.cross(wea,ra)
            if np.linalg.norm(vea)!=0:
                vea=np.dot(vea,vea_tgh)*vea_tgh/np.linalg.norm(vea)
        if b.mass==np.inf:
            web=np.array([0,0,0])
            veb=np.array([0,0,0])
        else:
            web=np.dot(np.linalg.inv(np.diag(b.inertia)),np.cross(-veb_tgh,rb))
            veb=veb_tgh/b.mass+np.cross(web,rb)
            if np.linalg.norm(veb)!=0:
                veb=np.dot(veb,veb_tgh)*veb_tgh/np.linalg.norm(veb)
        for i in range(0,3):
            if veb[i]-vea[i]!=0:
                count_I=(-1-kBiasFactor)*dv_x[i]/(veb[i]-vea[i])
        Im=count_I*vea_tgh
        # if np.dot(Im,va)>0 or (np.dot(Im,va)==0 and np.dot(Im,vb)>0):Im=-Im
        woa+=np.dot(np.linalg.inv(np.diag(a.inertia)),np.cross(Im,ra))
        wob-=np.dot(np.linalg.inv(np.diag(b.inertia)),np.cross(Im,rb))
        voa+=Im/a.mass
        vob-=Im/b.mass
        vva=np.linalg.norm(voa)
        vvb=np.linalg.norm(vob)
        pa=np.array(a.position)+d_tgh*vva*vea_tgh/(vva+vvb)
        pb=np.array(b.position)-d_tgh*vvb*veb_tgh/(vva+vvb)
        d1={'position':pa.tolist(),'velocity':voa.tolist(),'agl_v':woa.tolist()}
        d2={'position':pb.tolist(),'velocity':vob.tolist(),'agl_v':wob.tolist()}
        return d1,d2
    pass
