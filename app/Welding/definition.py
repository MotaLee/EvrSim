import os,time,json,math
import cv2
import numpy as np
import matplotlib.pyplot as plt
import urllib.request as url
class MtImg(object):
    ''' Opencv image class.'''
    def __init__(self,**argkw):

        if 'pimg' in argkw:
            if isinstance(argkw['pimg'],str):argkw['src']=argkw['pimg']
            elif isinstance(argkw['pimg'],np.ndarray):argkw['data']=argkw['pimg']
        if 'src' in argkw:
            self.data=cv2.imread(argkw['src'])
        elif 'data' in argkw:
            self.data=argkw['data']
        self.shape=self.data.shape
        self.height,self.width=self.shape[0:2]

        return

    def save(self,path):
        cv2.imwrite(path,self.data)
        return


    pass

class MtVid(object):
    def __init__(self,**argkw) -> None:
        self.src=argkw.get('src','')
        self.clip=argkw.get('clip',[0,0,0,0])
        self.vid=None
        self.idx_frame=0
        self.load()
        return

    def load(self):
        self.vid=cv2.VideoCapture(self.src)
        self.fps=self.vid.get(5)
        self.count=self.vid.get(7)
        self.time=self.count/self.fps
        return

    def release(self):
        if isinstance(self.vid,cv2.VideoCapture):
            self.idx_frame=0
            self.vid.release()
        return

    def next(self):
        frame=None
        if self.vid.isOpened():
            ret,frame=self.vid.read()
            if ret:
                self.idx_frame+=1
                frame:np.ndarray=frame[
                    self.clip[0]:frame.shape[0]-self.clip[1],
                    self.clip[2]:frame.shape[1]-self.clip[3]]
        return frame

    def getframe(self,idx):
        if idx<self.idx_frame:
            self.release()
            self.load()
        while(self.vid.isOpened()):
            ret,frame=self.vid.read()
            if self.idx_frame==idx:
                if frame is None:return None
                frame:np.ndarray=frame[
                    self.clip[0]:frame.shape[0]-self.clip[1],
                    self.clip[2]:frame.shape[1]-self.clip[3]]
                return frame
            else:self.idx_frame+=1
        return None

    pass

class FuncX2(object):
    def __init__(self,dt,t=0,a=0,b=0,c=0) -> None:
        self.a=a
        self.b=b
        self.c=c
        self.dt=dt
        self.t=t
        self.v=0
        return

    def next(self):
        self.v=self.a*self.t**2+self.b*self.t+self.c
        self.t+=self.dt
        return self.v
    pass

class FuncX3(object):
    def __init__(self,dt,t=0,a=0,b=0,c=0,d=0) -> None:
        self.a=a
        self.b=b
        self.c=c
        self.d=d
        self.dt=dt
        self.t=t
        self.v=0
        return

    def next(self):
        self.v=self.a*self.t**3+self.b*self.t**2+self.c*self.t+self.d
        self.t+=self.dt
        return self.v
    pass

class StereoCamConf(object):
    def __init__(self,**argkw):
        ''' Para:
           *Argkw json: Load config from json file;
           *Argkw imgs_left: Images form left camera;
           *Argkw imgs_right: Images form right camera;
            '''
        if 'json' in argkw:self.loadFromJson(argkw['json'])
        if 'imgs_left' in argkw:
            # self.R,self.T=ret
            pass
        return

    def loadFromJson(self,path):
        fd=open(path,'r')
        # txt=fd.read()
        conf=json.load(fd)
        self.width=np.array(conf['width'])
        self.height=np.array(conf['height'])
        # self.real_w=np.array(conf['real_w'])
        # self.real_h=np.array(conf['real_h'])
        self.Kl=np.array(conf['Kl'])
        self.Kr=np.array(conf['Kr'])
        self.Dl=np.array(conf['Dl'])
        self.Dr=np.array(conf['Dr'])
        self.R=np.array(conf['R'])
        self.T=np.array(conf['T'])
        self.focal=conf['focal']
        self.baseline=conf['baseline']
        self.pts_camr=np.array([self.baseline/2,.0,.0])
        self.pts_caml=np.array([-self.baseline/2,.0,.0])
        self.ppmlx=self.Kl[0][0]/self.focal     # Pixel per mm left x;
        self.ppmly=self.Kl[1][1]/self.focal
        self.ppmrx=self.Kr[0][0]/self.focal
        self.ppmry=self.Kr[1][1]/self.focal
        return

    pass

class CurveFeature(object):
    def __init__(self,**argkw) -> None:
        self.ctr_ori=argkw.get('ctr',None)
        if self.ctr_ori is None:return
        self.ctr_ori=self.ctr_ori.reshape(self.ctr_ori.size//2,2)
        self.ctr=cv2.approxPolyDP(self.ctr_ori,3,False)
        self.ctr=self.ctr.reshape(self.ctr.size//2,2)
        self.len=len(self.ctr)
        self.rect=cv2.boundingRect(self.ctr)
        self.center=np.array([self.rect[0]+self.rect[2]//2,self.rect[1]+self.rect[3]//2])
        self.offset=self.ctr[0]

        # ctr_ori=[[pt[0]-self.offset[0],pt[1]-self.offset[1]] for pt in self.ctr]
        self.ctr_off=self.ctr-self.offset
        self.rect_off=cv2.boundingRect(self.ctr_off)
        self.center_off=self.center-self.offset
        return
    pass

def cmpCurve(f1:CurveFeature,f2:CurveFeature,similar=True):
    if f1.len<f2.len:
        tmp=f1
        f1=f2
        f2=tmp
    if similar:'todo'
    list_d=list()
    for pt1 in f1.ctr_off:
        d=min([(pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2 for pt2 in f2.ctr_off])
        list_d.append(d)
    e=-sum(list_d)/len(list_d)
    if e<-100:return 0
    out=math.exp(e)
    return out

def simplifyCurve(pts:np.ndarray):

    return pts

def checkImgPara(pimg):
    ''' Check img parameter inputing to method.
        Support para type:
       *`str`: img source path;
       *`CvImg`: Original CvImg instance;'''
    if isinstance(pimg,MtImg):out=pimg
    elif isinstance(pimg,str):out=MtImg(src=pimg)
    elif isinstance(pimg,np.array):out=MtImg(data=pimg)
    return out

def getStreamImg(host='',port=8080):
    if not host:
        host='http://'+c.pi_host+':'+str(port)+'/?action=snapshot'
    stream=url.urlopen(host)
    bytes=b''
    bytes+=stream.read()
    a=bytes.find(b'\xff\xd8')
    b=bytes.find(b'\xff\xd9')
    if a!=-1 and b!=-1:
        jpg=bytes[a:b+2]
        # bytes= bytes[b+2:]
        # flags=1 for color image
        imgdata=cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),flags=1)
        img=MtImg(data=imgdata)
        # print i.shape
        # cv2.imshow("xiaorun",img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # if cv2.waitKey(1) & 0xFF == ord('q'):
            # return 0
    else:img=None
    return img

def capBicamImgs(**argkw):
    ''' Get Bicam images from MT stream.
       *Argkw portl: 8080 default;
       *Argkw portr: 8081 default;
       *Argkw host: MT host. Empty default;
       *Argkw save: Saving path. Empty default for not saving;
        '''
    host=argkw.get('host','')
    portl=argkw.get('portl',8080)
    portr=argkw.get('portr',8081)
    imgl=getStreamImg(host,portl)
    imgr=getStreamImg(host,portr)
    path=argkw.get('save','')
    if path!='':
        date=time.strftime("%Y%m%d%H%M%S", time.localtime())
        imgl.save(path+'\\BICAM-'+date+'-left.png')
        imgr.save(path+'\\BICAM-'+date+'-right.png')
    return imgl,imgr

def getIntrinsic(imgs,board=(6,4)):
    ''' Get Inner parameters of a cam from images.
       *Return: K/D;'''
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp=np.zeros((1,board[0]*board[1],3),dtype=np.float32)
    objp[0,:,:2]=np.mgrid[0:board[0],0:board[1]].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    pt_obj=[]    # 3d point in real world space
    pt_img=[]    # 2d points in image plane.
    if type(imgs)!=list:imgs=[imgs]
    for img in imgs:
        cvimg=checkImgPara(img)
        cvimg.data=cv2.cvtColor(cvimg.data,cv2.COLOR_BGR2GRAY)
        result, pt_corners=cv2.findChessboardCorners(cvimg.data,board,None)

        # If found, add object points, image points (after refining them)
        if result:
            result,corners2=cv2.find4QuadCornerSubpix(cvimg.data,pt_corners,(5,5))
            pt_obj.append(objp)
            pt_img.append(pt_corners)
            # showimg=cv2.drawChessboardCorners(cvimg,board, corners2,result)
            # cv2.imshow('img',showimg)
            # cv2.waitKey()

    N_OK=len(pt_obj)
    K=np.zeros((3, 3))
    D=np.zeros((5, 1))
    rvecs=[np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
    tvecs=[np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]

    ret, mtx, dist, rvecs, tvecs=cv2.calibrateCamera(
            pt_obj,pt_img,cvimg.shape[0:2][::-1],K,D,rvecs,tvecs,0)

    return mtx,dist,pt_obj,pt_img,rvecs,tvecs

def getBiCamPara(imgl,imgr,board=(6,4)):
    ''' Get parameters of a cam from images.
       *Return: K/D/rvecs/tvecs;'''
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    Kl,Dl,pt_obj,pt_imgl,rvecs,tvecs=getIntrinsic(imgl)
    Kr,Dr,pt_obj,pt_imgr,rvecs,tvecs=getIntrinsic(imgr)

    ret,Kl,Dl,Kr,Dr,R,T,E,F=cv2.stereoCalibrate(
        pt_obj,pt_imgl,pt_imgr,Kl,Dl,Kr,Dr,imgl[0].shape[0:2][::-1],flags=cv2.CALIB_FIX_INTRINSIC)
    return (Kl,Dl,Kr,Dr,R,T)

def getImgsInPath(path,filetype='png',kw=''):
    imgs=list()
    for fn in os.listdir(path):
        if filetype in fn and kw in fn:
            imgs.append(MtImg(src=path+'\\'+fn))
    return imgs

def showImg(img,wait=0):
    cv2.imshow('',img)
    cv2.waitKey(wait)
    return

def showList(y,x=None,block=True,pts=None):
    if not isinstance(x,np.ndarray):x=np.arange(0,len(y))
    plt.clf()
    plt.plot(x,y)
    if pts!=None:
        for pt in pts:
            plt.plot(pt[0],pt[1],'.y')
    plt.show(block=block)
    return plt

def showCurve(pts:np.ndarray):
    plt.clf()
    # plt.scatter(pts[:,1],pts[:,0])
    plt.plot(pts[:,1],pts[:,0])
    plt.show()
    # canvas=np.zeros((max(pts[:,1]),max(pts[:,0])))
    # for pt in pts:
    #     canvas=cv2.circle(canvas,pt,1,255,1)
    # showImg(canvas)
    return

def normalize(data):
    if not isinstance(data,np.ndarray):
        data=np.array(data)
    _range = np.max(data) - np.min(data)
    if _range==0:ret=data
    else:ret=(data - np.min(data)) / _range
    return ret

def drawCross(img:MtImg,pt):
    pt1=tuple(pt-np.array([10,0]))
    pt2=tuple(pt+np.array([10,0]))
    pt3=tuple(pt-np.array([0,10]))
    pt4=tuple(pt+np.array([0,10]))
    img.data=cv2.line(img.data,pt1,pt2,(0,255,0))
    img.data=cv2.line(img.data,pt3,pt4,(0,255,0))
    return img

def stretchMat(mat):
    mat:np.ndarray=cv2.normalize(mat,dst=None,alpha=350,beta=10,norm_type=cv2.NORM_MINMAX)
    return mat

def accumulateColumn(mat):
    y=np.ones((1,mat.shape[0]),dtype=np.int32)
    y=np.dot(y,mat)//mat.shape[0]
    y:np.ndarray=y.flatten()
    return y

def show3D(pts,ax=None,plot='scatter',block=True,clf=True):
    if ax==None:
        plt.ion()
        fig = plt.figure()
        from mpl_toolkits.mplot3d import Axes3D  # 空间三维画图
        ax = Axes3D(fig)

    if clf:ax.cla()
    if plot=='scatter':
        x=np.array([pt[0] for pt in pts])
        y=np.array([pt[1] for pt in pts])
        z=np.array([pt[2] for pt in pts])
        ax.scatter(x, y, z)
    elif plot=='wireframe':
        ptl=list()
        ptr=list()
        for i in range(len(pts)):
            if i%4==1 or i%4==0:ptl.append(pts[i])
            else:ptr.append(pts[i])
        xl=np.array([pt[0] for pt in ptl])
        xr=np.array([pt[0] for pt in ptr])
        yl=np.array([pt[1] for pt in ptl])
        yr=np.array([pt[1] for pt in ptr])
        zl=np.array([pt[2] for pt in ptl])
        zr=np.array([pt[2] for pt in ptr])
        # cl=[pt[1]**2+pt[2]**2 for pt in ptl]
        cl=[pt[0] for pt in ptl]
        cr=[pt[1]**2+pt[2]**2 for pt in ptr]
        cl=normalize(cl)
        cr=normalize(cr)
        rainbow=plt.get_cmap('rainbow').reversed()
        cl=np.array([rainbow(pt) for pt in cl])
        cr=np.array([rainbow(pt) for pt in cr])
        w=2
        h=len(xl)//2
        xl=xl.reshape(h,w)
        yl=yl.reshape(h,w)
        zl=zl.reshape(h,w)
        xr=xr.reshape(h,w)
        yr=yr.reshape(h,w)
        zr=zr.reshape(h,w)
        cl=cl.reshape(h,w,4)
        cr=cr.reshape(h,w,4)
        # ax.plot_wireframe(x,y,z)
        ax.plot_surface(xl,yl,zl,facecolors=cl)
        # ax.plot_surface(xr,yr,zr,facecolors=cr)

    ax.set_xlim3d(xmin=-50,xmax=50)
    ax.set_ylim3d(ymin=-125,ymax=125)
    ax.set_xlabel("Y")
    ax.set_ylabel("X")
    ax.set_zlabel("Z")
    plt.show(block=block)
    # plt.pause(10)
    plt.pause(1/25)
    return ax

def linkPoints(l,w=4,s=0):
    end=s+l
    edges=list()
    faces=list()
    for i in range(s,end):
        if i%w!=w-1:
            edges.append([i,i+1])
    for i in range(s,end-w-1):
        edges.append([i,i+4])
        faces.append([i,i+1,i+5,i+4])
    return edges,faces

def findCliffPt(mat,offx=0,offy=0,direction='left',pos=0,tor=10):
    ''' * Find cliff point in giving mat.
        ---
        Para:
        * mat: Source image matrix.
        * offx/offy: Offset of output point in outer image.
        * direction: Direction of searching point.
        * pos: Height position of searching.
        * tor: Tolerance of gap in search row.
        ---
        * Ret: Point or None;
        '''
    x=mat[pos:pos+1,:].flatten()
    ptx=None
    if direction=='left':
        for i in range(1,len(x)):
            if x[i]!=x[0]:
                forward=False
                for j in range(1,tor):
                    if i+j==len(x):break
                    if x[i+j]==x[0]:
                        forward=True
                        break
                if forward:i+=j
                else:ptx=i
                break
    else:
        for i in range(2,len(x)):
            if x[-i]!=x[-1]:
                forward=False
                for j in range(1,tor):
                    if i+j>len(x):break
                    if x[-i-j]==x[-1]:
                        forward=True
                        break
                if forward:i+=j
                else:ptx=len(x)-i
                break
    if ptx==None:pt=None
    else:pt=(offx+ptx,pos+offy)
    return pt

def findPeaks(x,mph=None,mpd=1,threshold=0,edge='rising',kpsh=False,valley=False):
    """ * Detect peaks in data based on their amplitude and other features.
        ---
        Para:
        * x : 1D array_like data.
        * mph : {None, number}; minimum peak height.
        * mpd : positive integer; minimum peak distance.
        * threshold : positive number;
            detect peaks (valleys) that are greater (smaller) than `threshold`.
        * edge : {None, 'rising', 'falling', 'both'};
            for a flat peak, keep only the rising edge ('rising'), only the
            falling edge ('falling'), both edges ('both'), or don't detect a
            flat peak (None).
        * kpsh : bool;
            keep peaks with same height even if they are closer than `mpd`.
        * valley : bool;
            if True (1), detect valleys (local minima) instead of peaks.
        ---
        * Ret: 1D array_like; indeces of the peaks in `x`.
        """
    x=np.atleast_1d(x).astype('float64')
    if x.size < 3:return np.array([], dtype=int)
    if valley:x=-x
    # find indexes of all peaks
    dx=x[1:] - x[:-1]
    # handle NaN's
    indnan=np.where(np.isnan(x))[0]
    if indnan.size:
        x[indnan]=np.inf
        dx[np.where(np.isnan(dx))[0]]=np.inf
    ine, ire, ife=np.array([[], [], []], dtype=int)
    if not edge:
        ine=np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) > 0))[0]
    else:
        if edge.lower() in ['rising', 'both']:
            ire=np.where((np.hstack((dx, 0)) <= 0) & (np.hstack((0, dx)) > 0))[0]
        if edge.lower() in ['falling', 'both']:
            ife=np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) >= 0))[0]
    ind=np.unique(np.hstack((ine, ire, ife)))
    # handle NaN's
    if ind.size and indnan.size:
        # NaN's and values close to NaN's cannot be peaks
        ind=ind[np.in1d(ind, np.unique(np.hstack((indnan, indnan-1, indnan+1))), invert=True)]
    # first and last values of x cannot be peaks
    if ind.size and ind[0] == 0:ind=ind[1:]
    if ind.size and ind[-1] == x.size-1:ind=ind[:-1]
    # remove peaks < minimum peak height
    if ind.size and mph is not None:ind=ind[x[ind] >= mph]
    # remove peaks - neighbors < threshold
    if ind.size and threshold > 0:
        dx=np.min(np.vstack([x[ind]-x[ind-1], x[ind]-x[ind+1]]), axis=0)
        ind=np.delete(ind, np.where(dx < threshold)[0])
    # detect small peaks closer than minimum peak distance
    if ind.size and mpd > 1:
        ind=ind[np.argsort(x[ind])][::-1]  # sort ind by peak height
        idel=np.zeros(ind.size, dtype=bool)
        for i in range(ind.size):
            if not idel[i]:
                # keep peaks with the same height if kpsh is True
                idel=idel | (ind >= ind[i] - mpd) & (ind <= ind[i] + mpd) \
                    & (x[ind[i]] > x[ind] if kpsh else True)
                idel[i]=0  # Keep current peak
        # remove the small peaks and sort back the indexes by their occurrence
        ind=np.sort(ind[~idel])
    return ind

def findBasin(x,width=20,height=8):
    x=normalize(x)*100
    # showList(x)
    pl=0
    pr=0
    w=0
    h=x[0]
    l=len(x)
    for i in range(1,l):
        if abs(x[i]-h)>height and w>width:break
        if x[i]>50 or abs(x[i]-h)>height:
            pl=i
            h=x[i]
            w=0
        elif abs(x[i]-h)<=height:
            pr=i
            w=pr-pl
        if i==l-1:
            pl=None
            pr=None
    return pl,pr

def hough(mat,show=False):
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(mat, 50, 100, apertureSize=3)  # apertureSize是sobel算子大小，只能为1,3,5，7
    showImg(edges)
    # lines = cv2.HoughLines(edges, 1, np.pi / 180, 50)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 25, minLineLength=20,maxLineGap=10)
    #函数将通过步长为1的半径和步长为π/180的角来搜索所有可能的直线
    if show and isinstance(lines,np.ndarray):
        for line in lines:
            # print(type(line))   #多维数组
            x1,y1,x2,y2 = line[0]
            # rho,theta = line[0]     #获取极值ρ长度和θ角度
            # a = np.cos(theta)       #获取角度cos值
            # b = np.sin(theta)       #获取角度sin值
            # x0 = a * rho    #获取x轴值
            # y0 = b * rho    #获取y轴值　　x0和y0是直线的中点
            # x1 = int(x0 + 1000*(-b))    #获取这条直线最大值点x1
            # y1 = int(y0 + 1000*(a))     #获取这条直线最大值点y1
            # x2 = int(x0 - 1000 * (-b))  #获取这条直线最小值点x2　　
            # y2 = int(y0 - 1000 * (a))   #获取这条直线最小值点y2
            mat=cv2.line(mat,(x1,y1),(x2,y2),128,2)
        # showImg(mat)
    return lines

def smoothLine(pts:list,thd=10,cut=True):
    l=len(pts)
    if l==0:return pts
    x=np.array([pt[1] for pt in pts])
    y=np.array([pt[0] for pt in pts])
    c=0
    while 1:
        c+=1
        if c==l:break
        A=np.vstack([x, np.ones(l)]).T
        k,b=np.linalg.lstsq(A, y,rcond=None)[0]
        d=list()
        sk=k**2+1
        for i in range(l):
            dis=(k*x[i]-y[i]+b)**2/sk
            d.append(dis)
        delta=max(d)-min(d)
        if delta<thd:break

        m=np.mean(d)
        if m-min(d)<max(d)-m:i=np.argmax(d)
        else:i=np.argmin(d)
        if cut:
            if i==0 or i==l-1:break
        if i+1>=l:r=0
        else:r=i+1
        pty=(pts[i-1][0]+pts[r][0])//2
        y[i]=pty
        pts[i][0]=pty
    return pts

def getMatRate(mat,nonzero=True):
    if nonzero==False:
        a=mat.size-np.count_nonzero(mat)
    elif nonzero==True:
        a=np.count_nonzero(mat)
    else:'todo'
    return a/mat.size

def findBasin2(x,width=20,height=8):
    x=normalize(x)*100
    x2=np.zeros(x.shape)
    # showList(x)
    pl=0
    pr=0
    w=0
    l=len(x)
    for i in range(l):
        if x[i]<=height:x2[i]=1
    for i in range(l):
        if x2[i]==1:
            pl=i
            break
    for i in range(1,l):
        if x2[-i]==1:
            pr=l-i
            break
    #     if abs(x[i]-h)>height and w>width:break
    #     if x[i]>50 or abs(x[i]-h)>height:
    #         pl=i
    #         h=x[i]
    #         w=0
    #     elif abs(x[i]-h)<=height:
    #         pr=i
    #         w=pr-pl
    #     if i==l-1:
    #         pl=None
    #         pr=None

    return pl,pr

def getLRCoff(self,pts):
    ''' Get linear regression coefficient.'''
    if not isinstance(pts,np.ndarray):
        pts=np.ndarray(pts)
    N = len(pts)
    x=pts[:,0]
    y=pts[:,1]
    sumx = sum(x)
    sumy = sum(y)
    sumx2 = sum(x**2)
    sumxy = sum(x*y)
    A = np.mat([[N, sumx], [sumx, sumx2]])
    b = np.array([sumy, sumxy])
    k,a=np.linalg.solve(A, b)
    return k,a
