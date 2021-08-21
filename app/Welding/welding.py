import sys,os,copy
import cv2
import numpy as np
sys.path.append(os.getcwd())    # for test
from app.Welding.definition import *
from app.Welding.depth import *

import matplotlib.pyplot as plt
rainbow=plt.get_cmap('rainbow')
class WeldingLabel(object):
    def __init__(self,**argkw) -> None:
        ''' * Welding label.
            ---
            Argkw:
            * src: Source to labeling, accept mtimg/vid/cam*.
            * wire: Wire point, None default.
            * groove: Welding groove type, auto default. Enum for auto/triangle/trapezoid/gap.
            * pool: If calculating welding pool. True default. If not pool, edges will be discard.
            * wait: Video frame waiting ms. 0 default for always stopping.
            '''
        self.src=''
        self.groove='auto'
        self.wait=0
        self.flag_pool=True
        self.radius=100
        self.dp=10

        self.pt_wire=None
        self.pts_pool=None
        self.uelx=-1     # Up edge left average x;
        self.uerx=-1
        self.delx=-1    # Down edge left average x;
        self.derx=-1
        self.pts_uel=list()   # Up edge left;
        self.pts_uer=list()
        self.pts_del=list()   # Down edge left;
        self.pts_der=list()

        self.idx_frame=0
        self.k3=np.ones((3,3), np.uint8)
        self.k5=np.ones((5,5), np.uint8)
        self.initLabel(**argkw)
        return

    def initLabel(self,**argkw):
        wire=argkw.get('wire',None)
        if wire!=None:
            self.pt_wire=np.array(wire,dtype=np.int32)
        self.src=argkw.get('src','')
        self.srctype=argkw.get('srctype','vid')
        self.groove=argkw.get('groove','auto')
        self.wait=argkw.get('wait',0)
        self.radius=argkw.get('radius',0)
        self.flag_pool=argkw.get('pool',True)
        self.dp=argkw.get('dp',10)
        self.dw=argkw.get('dw',20)
        self.dh=-1
        self.itvh=-1

        if self.src!='':
            if self.srctype=='vid':
                clip=argkw.get('clip',[0,0,0,0])
                self.vid=MtVid(src=self.src,clip=clip)
            else:
                self.pic=MtImg(src=self.src)
        return

    def drawImg(self,pimg=''):
        if isinstance(pimg,str):
            if pimg=='':pimg=self.src
        img=MtImg(pimg=pimg)
        self.getWeldingLabel(img)
        img=drawCross(img,self.pt_wire)
        # showImg(img.data)
        img.data=cv2.polylines(img.data,[self.pts_pool],True,(0,0,255),2)

        pts_lue=np.array(self.pts_uel,dtype=np.int32)
        img.data=cv2.polylines(img.data,[pts_lue],False,(255,255,0),2)
        pts_rue=np.array(self.pts_uer,dtype=np.int32)
        img.data=cv2.polylines(img.data,[pts_rue],False,(255,255,0),2)

        pts_del=np.array(self.pts_del,dtype=np.int32)
        img.data=cv2.polylines(img.data,[pts_del],False,(0,255,255),2)
        pts_der=np.array(self.pts_der,dtype=np.int32)
        img.data=cv2.polylines(img.data,[pts_der],False,(0,255,255),2)
        return img

    def showVid(self,src=''):
        ''' * Draw video via src.
            ---
            Para:
            * src: Source path to draw;'''
        if src!='':self.src=src
        while 1:
            frame=self.vid.next()
            # frame=drawCross(MtImg(data=frame),self.pt_wire)
            # showImg(frame.data)
            if frame is None:break
            img=self.drawImg(frame)
            cv2.imshow('',img.data)
            # showImg(img)
            if cv2.waitKey(self.wait) & 0xFF == ord('q'):
                break
        self.vid.release()
        cv2.destroyAllWindows()
        return

    def preprocess(self,img:MtImg):
        ''' Preprocess, including resize/converting to gray/adjust contrast;'''
        mat=img.data.copy()
        mat=cv2.cvtColor(mat,cv2.COLOR_RGB2GRAY)
        mat=stretchMat(mat)
        self.dh=mat.shape[0]//self.dp
        self.itvh=mat.shape[0]//self.dh
        return mat

    def getUpEdge(self,mat,wire,method='otsu'):
        y=accumulateColumn(mat)
        yl=y[:wire[0]]
        yr=y[wire[0]:]
        dyl=[(yl[i+2]-yl[i-2])/2 for i in range(2,len(yl)-2)]
        dyr=[(yr[i+2]-yr[i-2])/2 for i in range(2,len(yr)-2)]
        dyl=[.0,.0]+dyl+[.0,.0]
        dyr=[.0,.0]+dyr+[.0,.0]
        dylm=max(dyl)/3
        dyrm=min(dyr)/3
        peaks=list()
        i=20
        while i:
            i-=1
            peaks=findPeaks(dyl,dylm,5)
            if len(peaks)>3:
                if i>3:dylm+=0.5
                elif peaks[0]*2<peaks[1]:
                    exl=peaks[0]
                    break
            elif len(peaks)==0:dylm-=0.5
            elif wire[0]-peaks[0]<30:
                i=2
                dylm-=0.2
            else:
                exl=peaks[0]
                break
        peaks=list()
        while 1:
            peaks=findPeaks(dyr,-dyrm,5,valley=True)
            if len(peaks)>3:dyrm-=0.5
            elif len(peaks)==0:dyrm+=0.5
            else:
                exr=wire[0]+peaks[-1]
                break
        pts_uel=list()
        pts_uer=list()
        if exl-self.dw<0:img_lc=mat[:,0:2*self.dw]
        else:img_lc=mat[:,exl-self.dw:exl+self.dw]
        if exr+self.dw>=mat.shape[1]:img_rc=mat[:,0:2*self.dw]
        else:img_rc=mat[:,exr-self.dw:exr+self.dw]
        img_lc=stretchMat(img_lc)
        img_rc=stretchMat(img_rc)
        for i in range(self.itvh+1):
            hi=i*self.dh
            if i==self.itvh:
                img_ls=img_lc[hi:,:]
                img_rs=img_rc[hi:,:]
            else:
                img_ls=img_lc[hi:hi+self.dh,:]
                img_rs=img_rc[hi:hi+self.dh,:]
            if img_ls.size==0 or img_ls.size==0:break
            if i==0:rsy=0
            elif i==self.itvh-1:rsy=img_ls.shape[0]-2
            else:rsy=self.dh//2
            if method=='otsu':
                # yl=accumulateColumn(img_ls)
                # showList(yl)
                ret,img_ls=cv2.threshold(img_ls,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                ret,img_rs=cv2.threshold(img_rs,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                img_ls=cv2.morphologyEx(img_ls, cv2.MORPH_OPEN,self.k3,iterations=2)
                img_rs=cv2.morphologyEx(img_rs, cv2.MORPH_OPEN,self.k3,iterations=2)
            # if i==0:img_o=img_ls
            # else:img_o=np.vstack((img_o,img_ls))
            pt=None
            cl1=abs(getMatRate(img_ls)-0.5)<0.2 \
                and getMatRate(img_ls[:,img_ls.shape[1]-1:])>0.9
            if cl1:
                pt=findCliffPt(img_ls,exl-self.dw,hi,'right',rsy)
            else:
                pt=[exl,hi+rsy]
            if len(self.pts_uel)>i:
                if pt==None:
                    pt=(self.pts_uel[i][0]+exl-self.uelx,self.pts_uel[i][1])
                elif abs(pt[0]-self.pts_uel[i][0])>10:
                    # showImg(img_ls)
                    pt=(self.pts_uel[i][0]+exl-self.uelx,self.pts_uel[i][1])
            if pt!=None:pts_uel.append(pt)

            pt=None
            cr1=abs(np.count_nonzero(img_rs)/img_rs.size-0.5)<0.2 \
                and np.count_nonzero(img_rs[:,0:1])/img_rs.shape[0]>0.9
            if cr1:
                pt=findCliffPt(img_rs,exr-self.dw,hi,'left',rsy)
            else:
                pt=[exr,hi+rsy]
            if len(self.pts_uer)>i:
                if pt==None:
                    pt=(self.pts_uer[i][0]+exr-self.uerx,self.pts_uer[i][1])
                elif abs(pt[0]-self.pts_uer[i][0])>10:
                    pt=(self.pts_uer[i][0]+exr-self.uerx,self.pts_uer[i][1])
            if pt!=None:pts_uer.append(pt)
        return pts_uel,pts_uer,exl,exr

    def getPool(self,mat,wire,exl,exr):
        pts_pool=None
        rect_pool=None
        img_s2=mat[mat.shape[0]//2:,exl+5:exr-5]
        ret,img_otsu=cv2.threshold(img_s2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        ret,img_s2=cv2.threshold(img_s2,ret-5,255,cv2.THRESH_BINARY)
        img_s2=np.vstack((np.zeros(img_s2.shape),img_s2)).astype(np.uint8)
        # showImg(img_s2)
        ctrs,hierarchy=cv2.findContours(img_s2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for ctr in ctrs:
            rect=cv2.boundingRect(ctr)
            c1=exl+rect[0]<wire[0]
            c2=exl+rect[0]+rect[2]>wire[0]
            c3=rect[1]<wire[1]
            c4=rect[1]+rect[3]>wire[1]
            c5=rect[3]<0.5*mat.shape[0]
            if c1&c2&c3&c4&c5:
                rect_pool:np.ndarray=rect
                pts_pool:np.ndarray=ctr
                # pts_pool=cv2.approxPolyDP(ctr,3,True)
                rect_pool=list(rect_pool)
                rect_pool[0]+=exl+5
                for pt in pts_pool:
                    pt[0][0]+=exl+5
                break
        if not isinstance(pts_pool,np.ndarray):
            pts_pool=None
            rect_pool=None
        return pts_pool,rect_pool

    def getDownEdge(self,mat,tpl):
        pts_del=list()
        pts_der=list()
        pts_uel,pts_uer,exl,exr,pts_pool,rect_pool=tpl
        if self.groove=='auto':pass
        elif self.groove=='trapezoid':pass
        elif self.groove=='gap':
            for i in range(self.itvh):
                hi=i*self.dh
                if rect_pool is not None:
                    if hi>rect_pool[1]-50:continue
                if i==self.itvh:
                    img_gap=mat[hi:,pts_uel[i][0]+5:pts_uer[i][0]-5]
                else:
                    img_gap=mat[hi:hi+self.dh,pts_uel[i][0]+5:pts_uer[i][0]-5]
                if img_gap.size==0:break
                if i==0:rsy=2
                elif i==self.itvh-1:rsy=img_gap.shape[0]-2
                else:rsy=self.dh//2
                y=accumulateColumn(img_gap)
                # y=np.ones((1,img_gap.shape[0]),dtype=np.int32)
                # y=np.dot(y,img_gap)//img_gap.shape[0]
                # y=y.flatten()
                width=15
                while 1:
                    ptlx,ptrx=findBasin2(y,width,(max(y)-min(y))/10)
                    if ptlx!=None or width<5:
                        break
                    else:width-=3
                # showList(y,pts=[[ptlx,0],[ptrx,0]])
                if ptlx!=None:
                    ptl=[pts_uel[i][0]+5+ptlx-3,hi+rsy]
                    ptr=[pts_uel[i][0]+5+ptrx+3,hi+rsy]
                else:
                    ptl=None
                    ptr=None
                if len(self.pts_del)>i:
                    if ptl==None:
                        ptl=self.pts_del[i]
                    elif abs(ptl[0]-self.pts_del[i][0])>7:
                        ptl=self.pts_del[i]
                if ptl!=None:pts_del.append(ptl)
                if len(self.pts_der)>i:
                    if ptr==None:
                        ptr=self.pts_der[i]
                    elif abs(ptr[0]-self.pts_der[i][0])>7:
                        ptr=self.pts_der[i]
                if ptr!=None:pts_der.append(ptr)
        elif self.groove=='triangle':
            if isinstance(pts_pool,np.ndarray):
                n_pt=rect_pool[1]//self.dh-1
                xl=max([pts_uel[i][0] for i in range(n_pt)])
                xr=min([pts_uer[i][0] for i in range(n_pt)])
                img_center=mat[:n_pt*self.dh,xl+5:xr-5]
            else:
                xl=exl
                xr=exr
                img_center=mat[:,xl+5:xr-5]
            img_center=cv2.Canny(img_center,15,30)
            y=accumulateColumn(img_center)
            # y=np.ones((1,img_center.shape[0]),dtype=np.int32)
            # y=np.dot(y,img_center)/img_center.shape[0]
            # y=y.flatten()
            peaks=findPeaks(y,50)
            if len(peaks)>=2:
                self.delx=min(peaks)
                self.derx=max(peaks)
            else:
                'todo'
                pass
            for i in range(n_pt):
                img_s=img_center[pts_uel[i][1]:pts_uel[i][1]+1,self.delx-5:self.delx+5]
                img_s=img_s.flatten()
                ptlx=np.argmax(img_s)+self.delx+xl
                ptrx=np.argmax(img_s)+self.derx+xl
                pts_del.append([ptlx,pts_uel[i][1]])
                pts_der.append([ptrx,pts_uel[i][1]])
        return pts_del,pts_der

    def getWeldingLabel(self,img:MtImg,overlay=True):
        ''' * Get labels of welding, including wire point/pool area/edges.
            ---
            * img: Image to label.
            * wire: False default for not using inner wire point.
            * overlay: If True, inner label data will be overlayed by this labeling.
            ---
            * Ret: A tuple forms like (pt_wp,pts_pool,pts_lue,pts_rue);'''
        img_mat=self.preprocess(img)
        pt_wire=self.pt_wire
        # Label upper edge;
        pts_uel,pts_uer,exl,exr=self.getUpEdge(img_mat,pt_wire)
        # Label pool area, and judge if welding;
        if self.flag_pool:
            pts_pool,rect_pool=self.getPool(img_mat,pt_wire,exl,exr)
            flag_welding=isinstance(pts_pool,np.ndarray)
            if not flag_welding:
                pts_uel=list()
                pts_uer=list()
            else:
                if exl>rect_pool[0]:
                    pts_uel=list(self.pts_uel)
                else:self.uelx=exl
                if exr<rect_pool[0]+rect_pool[2]:
                    pts_uer=list(self.pts_uer)
                else:self.uerx=exr
        else:
            self.uelx=exl
            self.uerx=exr
            pts_pool=None
            rect_pool=None
            flag_welding=False
        # Label lower edge;
        if self.groove and isinstance(pts_uel,list) and (flag_welding or not self.flag_pool):
            tpl=pts_uel,pts_uer,exl,exr,pts_pool,rect_pool
            pts_del,pts_der=self.getDownEdge(img_mat,tpl)
        else:
            pts_del=list()
            pts_der=list()
        # Postprocess;
        if self.radius>500:
            pts_del=smoothLine(pts_del,thd=7,cut=False)
            pts_der=smoothLine(pts_der,thd=7,cut=False)
        else:
            pts_del=smoothLine(pts_del[:len(pts_del)//2],thd=7)+smoothLine(pts_del[len(pts_del)//2:],thd=7)
            pts_der=smoothLine(pts_der[:len(pts_der)//2],thd=7)+smoothLine(pts_der[len(pts_der)//2:],thd=7)
        if overlay:
            if isinstance(pts_pool,np.ndarray):self.pts_pool=pts_pool
            if isinstance(pts_uel,list):self.pts_uel=pts_uel
            if isinstance(pts_uer,list):self.pts_uer=pts_uer
            if isinstance(pts_del,list):self.pts_del=pts_del
            if isinstance(pts_der,list):self.pts_der=pts_der
        return [pt_wire,pts_pool,pts_uel,pts_uer,pts_del,pts_der]

    def checkParallel(self):
        ptl=self.pts_uel
        ptr=self.pts_uer
        kl,bl=getLRCoff(ptl)
        kr,br=getLRCoff(ptr)
        dagl=abs(np.arctan(kl)-np.arctan(kr))
        return dagl

    pass

class StereoWelding(object):
    def __init__(self,**argkw) -> None:
        self.label_l=WeldingLabel()
        self.label_r=WeldingLabel()

        self.conf=StereoCamConf(json='app\\Welding\\conf\\cam_blender.json')
        self.pt3_wire=None
        self.ratio=argkw.get('ratio',1)
        self.agl=argkw.get('speed',FuncX3(1/25,d=1)) # rad/s, constance or function;
        self.frame=0
        self.radius=0
        self.vidl=None
        self.vidr=None
        self.pta=None
        return

    def linkPoints(self,pts,column=4,close=False):
        edges=list()
        faces=list()
        l=len(pts)
        cm1=column-1
        chm1=column/2-1
        for i in range(l-1):
            if i%column!=cm1 or i%column!=chm1:
                edges.append((i,i+1))
        for i in range(l-column):
            edges.append((i,i+4))
            if i%column==0 or i%column==chm1+1:
                faces.append((i,i+1,i+5,i+4))
        if close:
            'todo'
        return edges,faces

    def rebuildImg(self,iml,imr,save=''):
        retl=self.label_l.getWeldingLabel(iml)
        retr=self.label_r.getWeldingLabel(imr)
        len_de=len(retr[4])
        if len(retl[2])>len_de:
            retl[2]=retl[2][:len_de]
            retl[3]=retl[3][:len_de]
        pts=list()
        for i in range(len(retl[2])):
            pt_uel=self.getPoint3(retl[2][i],retr[2][i]).tolist()
            pt_del=self.getPoint3(retl[4][i],retr[4][i]).tolist()
            pt_der=self.getPoint3(retl[5][i],retr[5][i]).tolist()
            pt_uer=self.getPoint3(retl[3][i],retr[3][i]).tolist()
            pts+=[pt_uel,pt_del,pt_der,pt_uer]
        # show3D(pts,'wireframe')
        if save!='':
            fd=open(save,'w')
            txt_pts=str(pts)
            edges,faces=self.linkPoints(pts)
            txt_edges=str(edges)
            txt_faces=str(faces)
            txt_pts=txt_pts.replace(', [',',\n    [')
            txt_edges=txt_edges.replace(', (',',\n    (')
            txt_faces=txt_faces.replace(', (',',\n    (')
            txt='pts='+txt_pts+\
                '\nedges='+txt_edges+\
                '\nfaces='+txt_faces
            fd.write(txt)
            fd.close()
        return pts

    def getPoint3(self,ptl,ptr):
        ratio=self.ratio
        conf=self.conf
        dx=(ptl[0]-ptr[0])*ratio
        dxl=ptl[0]*ratio-conf.width//2
        dyl=ptl[1]*ratio-conf.height//2
        pt3=conf.pts_caml.copy()
        x=dxl*conf.baseline/dx
        y=dyl*conf.baseline/dx
        z=conf.ppmlx*conf.focal*62/dx
        pt3[0]+=x
        pt3[1]=-pt3[1]-y
        pt3[2]-=z
        return pt3

    def rebuildFrame(self,idx=0,save=''):
        framel=self.label_l.vid.getFrame(idx)
        framer=self.label_r.vid.getFrame(idx)
        iml=MtImg(data=framel)
        imr=MtImg(data=framer)
        self.rebuildImg(iml,imr,save)
        return

    def rebuildNextFrame(self,color=True):
        if self.radius==0:
            self.radius=self.label_l.radius
            self.vidl=self.label_l.vid
            self.vidr=self.label_r.vid
        self.frame+=1
        framel=self.vidl.next()
        framer=self.vidr.next()
        if framel is None:return
        iml=MtImg(data=framel)
        imr=MtImg(data=framer)
        pts=np.array(self.rebuildImg(iml,imr)).transpose()
        pts[2,:]+=self.radius
        ones=np.ones((1,pts.shape[1]))
        pts=np.vstack((pts,ones))
        agl=self.agl.next()
        c=np.cos(-agl)
        s=np.sin(-agl)
        mat_trans=np.array([
            [1,0,0,0],
            [0,c,-s,0],
            [0,s,c,0],
            [0,0,0,1]])
        pts=np.dot(mat_trans,pts)/25
        pts=pts[0:3,:].transpose()
        c=np.ones((pts.shape[0],4))
        if color:
            dlist=[pts[i][1]**2+pts[i][2]**2 for i in range(len(pts))]
            dlist=normalize(dlist)
            for i in range(len(pts)):
                c[i]=rainbow(dlist[i])
        pts=np.hstack((pts,c))
        if agl==0:
            self.pta=pts
        else:
            self.pta=np.hstack((self.pta,pts))
        return pts

    def rebuildAfterWelding(self,iml,imr,subyx=(2,4)):
        ''' Match Template.'''
        retl=self.label_l.getWeldingLabel(iml)
        retr=self.label_r.getWeldingLabel(imr)
        ptsll=retl[2]
        ptslr=retl[3]
        subptsll=list()
        subptslr=list()
        dh=int((ptsll[1][1]-ptsll[0][1])/(subyx[0]+1))
        n_ptsll=len(ptsll)
        for i in range(n_ptsll):
            subptsll.append(ptsll[i])
            subptslr.append(ptslr[i])
            if i!=n_ptsll-1:
                dwl=(ptsll[i][0]-ptsll[i+1][0])/(subyx[0]+1)
                dwr=(ptslr[i][0]-ptslr[i+1][0])/(subyx[0]+1)
                subptsll+=[[
                    int(dwl*j+ptsll[i][0]),
                    int(dh*j+ptsll[i][1])]
                    for j in range(1,subyx[0]+1)]
                subptslr+=[[
                    int(dwr*j+ptslr[i][0]),
                    int(dh*j+ptslr[i][1])]
                    for j in range(1,subyx[0]+1)]
        gridl=list(subptsll)
        for i in range(1,subyx[1]+1):
            for j in range(len(subptsll)):
                dx=(subptslr[j][0]-subptsll[j][0])/(subyx[1]+1)
                gridl.append([subptsll[j][0]+int(i*dx),subptsll[j][1]])
        gridl+=subptslr
        gridr=copy.deepcopy(gridl)
        col=2+subyx[1]
        row=len(gridr)//col
        idx_rt=(col-1)*row
        for i in range(len(gridr)):
            if i//row==0:
                if i%3==0:gridr[i]=retr[2][i//3]
                else:gridr[i][0]=gridr[i-1][0]
            elif i//row==col-1:
                if (i-idx_rt)%3==0:gridr[i]=retr[3][(i-idx_rt)//3]
                else:gridr[i][0]=gridr[i-1][0]

        imlc=cv2.Canny(iml.data,50,100)
        imlc[:,:self.label_l.uelx+5]=0
        imlc[:,self.label_l.uerx-5:]=0
        ctrs,hierarchy=cv2.findContours(imlc,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        imlc=np.zeros(imlc.shape,dtype=np.uint8)
        linel=list()
        for ctr in ctrs:
            rect=cv2.boundingRect(ctr)
            if rect[2]<20 and rect[3]<20:continue
            ctr=ctr.reshape((ctr.size//2,2))
            linel.append(ctr)
        imlc=cv2.drawContours(imlc,linel,-1,255,1)
        imrc=cv2.Canny(imr.data,50,100)
        imrc[:,:self.label_r.uelx+5]=0
        imrc[:,self.label_r.uerx-5:]=0
        ctrs,hierarchy=cv2.findContours(imrc,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        imrc=np.zeros(imrc.shape,dtype=np.uint8)
        liner=list()
        for ctr in ctrs:
            rect=cv2.boundingRect(ctr)
            if rect[2]<20 and rect[3]<20:continue
            ctr=ctr.reshape((ctr.size//2,2))
            liner.append(ctr)
        imrc=cv2.drawContours(imrc,liner,-1,255,1)

        h2=dh//2
        w2=(gridl[1][1]-gridl[0][1])//2
        l=len(gridl)
        idxl=self.label_r.uelx+5
        idxr=self.label_r.uerx-5
        for i in range(l):

            if i//row==0 or i//row==col-1:continue
            if i%row==0 or i%row==row-1:continue

            tmp=imlc[gridl[i][1]-h2:gridl[i][1]+h2,gridl[i][0]-w2:gridl[i][0]+w2]
            tar_row=imrc[gridl[i][1]-h2:gridl[i][1]+h2,gridr[i-row][0]:idxr]
            tm=cv2.matchTemplate(tar_row,tmp,cv2.TM_CCOEFF)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(tm)
            gridr[i][0]=max_loc[0]+gridr[i-row][0]+w2

        # showImg(np.vstack((tmp,row[:,max_loc[0]:max_loc[0]+dh])))
        # img=imlc+imrc
        # for pt in gridl+gridr:
        #     img=cv2.circle(img,tuple(pt),2,255,2)
        # showImg(img)
        gridl=np.array(gridl)[1:-1,:]
        gridr=np.array(gridr)[1:-1,:]
        return
    pass

# Debug
# wl=WeldingLabel()
# wl.initLabel(wire=[195,270],src='app\\Welding\\vid\\GMAW.1层焊道摆动.垂直.ts',
    # wait=50,groove='triangle',clip=[30,20,0,0])
# wl.initLabel(wire=[675,400],src='app\\Welding\\vid\\blender-left.mp4',
#     wait=50,groove='gap',pool=False,clip=[5,5,0,0])
# wl.initLabel(wire=[955,600],src='app\\Welding\\vid\\blender-l2.mp4',
#     wait=50,groove='gap',pool=False,clip=[5,5,0,0],radius=1016)
# wl.initLabel(wire=[325,600],src='app\\Welding\\pic\\r3.png',srctype='pic',wait=50,groove='gap',pool=False,clip=[5,5,0,0],radius=1016)
# wl.initLabel(wire=[180,400],src='app\\Welding\\vid\\blender-right.mp4',
#     wait=50,groove='gap',pool=False,clip=[5,5,0,0])
# wl.initLabel(wire=[323,460],src='app\\Welding\\vid\\Blender-AE-Welding.mp4',
#     wait=50,groove='gap',clip=[0,220,0,0])
# wl.showVid()
# src='app\\Welding\\pic\\blender-after-left.png'
# wl.initLabel(wire=[1000,600],src=src,srctype='pic',pool=False,groove=False)
# tpl=wl.getWeldingLabel(wl.pic)
# showImg(wl.drawImg().data)

# T=20
# a=-12*np.pi/T**3
# b=12*np.pi/T**2
# sw=StereoWelding(ratio=1.5,speed=FuncX2(1/25,0,a,b))
# sw.label_l.initLabel(wire=[675,400],src='res\\vid\\blender-left.mp4',
#     wait=50,groove='gap',pool=False,clip=[5,5,0,0],radius=225)
# sw.label_r.initLabel(wire=[180,400],src='res\\vid\\blender-right.mp4',
#     wait=50,groove='gap',pool=False,clip=[5,5,0,0],radius=225)
# sw.rebuildPipe()
# pt3=sw.getPoint3([675,400],[180,400],ratio=1.5)
# print(pt3)

# iml=MtImg(src='app\\Welding\\pic\\blender-after-left.png')
# imr=MtImg(src='app\\Welding\\pic\\blender-after-right.png')
# conf=StereoCamConf(json='app\\Welding\\conf\\cam_blender.json')
# miml,mimr=getDepthImg(iml,imr,conf)
# showImg(miml.data)

sw=StereoWelding(ratio=1.5)
sw.label_l.initLabel(wire=[1000,600],src='app\\Welding\\pic\\blender-after-left.png',
    srctype='pic',pool=False,groove=False)
sw.label_r.initLabel(wire=[300,600],src='app\\Welding\\pic\\blender-after-right.png',
    srctype='pic',pool=False,groove=False)
sw.rebuildAfterWelding(sw.label_l.pic,sw.label_r.pic)
