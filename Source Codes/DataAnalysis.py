# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 22:43:57 2019

@author: kamrul
"""


import glob
import nibabel as nib
from matplotlib import pyplot as plt
import numpy as np
from skimage import data, color, io, img_as_float
import cv2
import os 

cwd = 'D:\KiTS Project\kits19\scripts'

dataPath = glob.glob('D:\KiTS Project\kits19\scripts\dataTrain\*');
dataPath.sort()

for i in range(len(dataPath)):
  
    org_vol = (nib.load(dataPath[i]+'\imaging.nii.gz')).get_fdata()
    
    mask_vol = (nib.load(dataPath[i]+'\segmentation.nii.gz')).get_fdata()

    kidney = mask_vol.copy()
    tumor = mask_vol.copy()

    kidney[kidney!=1]=0
    kidney[kidney==1]=255
    tumor[tumor!=2]=0
    tumor[tumor==2]=255


#    for k in range (300,400,1):
    for k in range (len(org_vol[:,1,1])):
        


        img_color = np.dstack((org_vol[k,:,:], org_vol[k,:,:], org_vol[k,:,:]))

        kidney_color = np.zeros_like(img_color)
        kidney_color[kidney[k,:,:]!=0] = [0, 0, 255] # Blue block
        
        tumor_color = np.zeros_like(img_color)
        tumor_color[tumor[k,:,:]!=0] = [0, 255, 0] # Blue block
        
        img_hsv_T = color.rgb2hsv(img_color)
        img_hsv_K = img_hsv_T.copy()
        kidney_color = color.rgb2hsv(kidney_color)
        tumor_color = color.rgb2hsv(tumor_color)
        
        img_hsv_K[:,:, 0] = kidney_color[:,:, 0]
        img_hsv_K[:,:, 1] = kidney_color[:,:, 1] * 0.6
        img_hsv_K = color.hsv2rgb(img_hsv_K)
        
        path = cwd + '\\ImageChecker\\' + dataPath[i][-10:] +'_'+str(k)+'_kidney_over.png'
        
        cv2.imwrite(path,img_hsv_K)

        img_hsv_T[:,:, 0] = tumor_color[:,:, 0]
        img_hsv_T[:,:, 1] = tumor_color[:,:, 1] * 0.6
        img_hsv_T = color.hsv2rgb(img_hsv_T)

        path = cwd + '\\ImageChecker\\' + dataPath[i][-10:] +'_'+str(k)+'_tumor_over.png'
        cv2.imwrite(path,img_hsv_T)
        
        
        
        path = cwd + '\\ImageChecker\\' + dataPath[i][-10:] +'_'+str(k)+'_kidney_.png'
        
        cv2.imwrite(path,kidney[k,:,:])
        
        path = cwd + '\\ImageChecker\\' + dataPath[i][-10:] +'_'+str(k)+'_tumor_.png'
        cv2.imwrite(path,tumor[k,:,:])
        
        path = cwd + '\\ImageChecker\\' + dataPath[i][-10:] +'_'+str(k)+'_mask_.png'
        cv2.imwrite(path,120*mask_vol[k,:,:])
        
        path = cwd + '\\ImageChecker\\' + dataPath[i][-10:] +'_'+str(k)+'_org_.png'
        cv2.imwrite(path,org_vol[k,:,:])
        
        
        
        print('Case-> '+str(i)+'   '+'slice-> '+str(k))
        
#    if i==5:
#    break
    
    
    




