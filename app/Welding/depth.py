import os,json,sys
import cv2
import numpy as np
from app.Welding.definition import MtImg,showImg,StereoCamConf

def getRectifyTransform(width,height,conf:StereoCamConf):
    # 获取畸变校正和立体校正的映射变换矩阵、重投影矩阵
    # 计算校正变换
    R1,R2,P1,P2,Q,roi1,roi2=cv2.stereoRectify(conf.Kl,conf.Dl,
        conf.Kr,conf.Dr,(width,height),conf.R,conf.T, alpha=0)
    map1x,map1y=cv2.initUndistortRectifyMap(conf.Kl,conf.Dl,
        R1, P1, (width, height), cv2.CV_32FC1)
    map2x,map2y=cv2.initUndistortRectifyMap(conf.Kr,conf.Dr,
        R2, P2, (width, height), cv2.CV_32FC1)
    mapxy=(map1x, map1y, map2x, map2y)
    return mapxy,Q

def undistort(img:MtImg,K,D):
    img.data=cv2.undistort(img.data,K,D)
    return img

def rectifyImage(iml,imr,mapxy):
    # 畸变校正和立体校正
    riml=cv2.remap(iml.data,mapxy[0],mapxy[1],cv2.INTER_AREA)
    rimr=cv2.remap(imr.data,mapxy[2],mapxy[3],cv2.INTER_AREA)
    return MtImg(data=riml),MtImg(data=rimr)

def drawRectifyLines(iml:MtImg,imr:MtImg):
    # 立体校正检验----画线
    # 建立输出图像
    height=iml.height
    width=iml.width+imr.width
    output=np.hstack((iml.data,imr.data))
    # 绘制等间距平行线
    itv=50      # 直线间隔：50
    for k in range(height//itv):
        cv2.line(output,
            (0,itv*(k+1)),
            (2*width,itv*(k+1)),
            (0,255,0),thickness=2,lineType=cv2.LINE_AA)
    return MtImg(data=output)

def preSGBM(img:MtImg):
    ''' Preprocess of SGBM to weaken the lighting affect.
        Convert color image to gray image, and equalize hist.'''
    # 预处理，一般可以削弱光照不均的影响，不做也可以
    # 彩色图->灰度图
    # 通过OpenCV加载的图像通道顺序是BGR
    img.data=cv2.cvtColor(img.data,cv2.COLOR_BGR2GRAY)
    # 直方图均衡
    img.data=cv2.equalizeHist(img.data)
    return img

def stereoMatchSGBM(iml:MtImg,imr:MtImg,down_scale=False):
    # 视差计算
    # SGBM匹配参数设置
    iml=iml.data
    imr=imr.data
    if iml.ndim == 2:img_channels=1
    else:img_channels=3
    blockSize=5
    paraml={'minDisparity': 0,
        'numDisparities': 128,
        'blockSize': blockSize,
        'P1': 8 * img_channels * blockSize ** 2,
        'P2': 32 * img_channels * blockSize ** 2,
        'disp12MaxDiff': 1,
        'preFilterCap': 7,
        'uniquenessRatio': 15,
        'speckleWindowSize': 100,
        'speckleRange': 1,
        'mode': cv2.StereoSGBM_MODE_HH4}
    # cv2.STEREO_SGBM_MODE_SGBM_3WAY
    # cv2.STEREO_SGBM_MODE_HH4
    # 构建SGBM对象
    left_matcher=cv2.StereoSGBM_create(**paraml)
    paramr=paraml
    paramr['minDisparity']=-paraml['numDisparities']
    right_matcher=cv2.StereoSGBM_create(**paramr)

    # 计算视差图
    size=(iml.shape[1], iml.shape[0])
    if down_scale == False:
        disparity_left=left_matcher.compute(iml, imr)
        disparity_right=right_matcher.compute(imr, iml)
    else:
        iml_down=cv2.pyrDown(iml)
        imr_down=cv2.pyrDown(imr)
        factor=iml.shape[1] / iml_down.shape[1]
        disparity_left_half=left_matcher.compute(iml_down, imr_down)
        disparity_right_half=right_matcher.compute(imr_down, iml_down)
        disparity_left=cv2.resize(disparity_left_half, size, interpolation=cv2.INTER_AREA)
        disparity_right=cv2.resize(disparity_right_half, size, interpolation=cv2.INTER_AREA)
        disparity_left=factor * disparity_left
        disparity_right=factor * disparity_right

    # 真实视差（因为SGBM算法得到的视差是×16的）
    trueDisp_left=disparity_left.astype(np.float32)/16
    trueDisp_right=disparity_right.astype(np.float32)/16+128
    tdl=MtImg(data=np.clip(trueDisp_left,0,127).astype(np.uint8))
    tdr=MtImg(data=np.clip(trueDisp_right,0,127).astype(np.uint8))
    return tdl,tdr

def fillHole(img:MtImg):
    width=img.width
    height=img.height
    data=img.data
    integralMap=data.copy().astype(np.float64)
    ptsMap=np.clip(data,0,1).astype(np.float64)
    integralMap=cv2.integral(integralMap)
    ptsMap=cv2.integral(ptsMap)
    dWnd=2
    while (dWnd > 1):
        wnd=int(dWnd)
        dWnd /= 2
        for i in range(height):
            for j in range(width):
                left=max(0,j-wnd-1)
                top=max(0,i-wnd-1)
                right=min(j+wnd, width-1)
                bot=min(i+wnd, height-1)
                ptsCnt=ptsMap[bot][right]+ptsMap[top][left]\
                    -(ptsMap[bot][left]+ptsMap[top][right])
                sumGray=integralMap[bot][right]+integralMap[top][left]\
                    -(integralMap[bot][left]+integralMap[top][right])
                if (ptsCnt <= 0):continue
                data[i][j]=sumGray/ptsCnt
        s=int(wnd/2*2+1)
        img.data=cv2.GaussianBlur(img.data,(s,s),s,s)
    cv2.imshow('',img.data)
    cv2.waitKey()
    return img

def getDepthImg(iml:MtImg,imr:MtImg,conf,save=False,linecheck=False):
    width=iml.width
    height=iml.height
    # conf=StereoCamConf(json='mem\\cam_real.json')
    iml=undistort(iml,conf.Kl,conf.Dl)
    imr=undistort(imr,conf.Kr,conf.Dr)
    # 立体校正
    mapxy,Q=getRectifyTransform(width,height,conf)
    riml,rimr=rectifyImage(iml,imr,mapxy)
    # print(Q)

    # 绘制等间距平行线，检查立体校正的效果
    if linecheck:
        line=drawRectifyLines(riml,rimr)
        showImg(line.data)

    # 立体匹配
    # iml=preSGBM(riml)
    # imr=preSGBM(rimr)
    # showImg(imr.data)
    miml,mimr=stereoMatchSGBM(riml,rimr)
    # miml=fillHole(miml)
    # mimr=fillHole(mimr)
    if save:
        cv2.imwrite(save+'-left.png',miml.data)
        cv2.imwrite(save+'-right.png',mimr.data)
    return miml,mimr
