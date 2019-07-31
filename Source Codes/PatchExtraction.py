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
from sklearn.feature_extraction.image import extract_patches_2d

PatchSavePath = 'D:\KiTS Project\kits19\scripts'

NumberPatch =100

dataPath = glob.glob('D:\KiTS Project\kits19\scripts\dataTrain\*');
dataPath.sort()

for i in range(len(dataPath)):
  
    org_vol = (nib.load(dataPath[i]+'\imaging.nii.gz')).get_fdata()
    
    mask_vol = (nib.load(dataPath[i]+'\segmentation.nii.gz')).get_fdata()
    
    for k in range (300,400,1):
        current_slice_org = org_vol[k,:,:]
        current_slice_mask = mask_vol[k,:,:]
        patches_current_slice_org = extract_patches_2d(current_slice_org, (256, 256),
                                        max_patches=NumberPatch, random_state=100)
        patches_current_slice_mask= extract_patches_2d(current_slice_mask, (256, 256),
                                                       max_patches=NumberPatch, random_state=100)
        
        for j in range(NumberPatch):
            path = PatchSavePath + '\\Patches\\' + dataPath[i][-10:]+'_'+str(k)+str(j)+'_org_.png'
            cv2.imwrite(path,patches_current_slice_org[j,:,:])
            
            path = PatchSavePath + '\\Patches\\' + dataPath[i][-10:]+'_'+str(k)+str(j)+'_mask_.png'
            cv2.imwrite(path,patches_current_slice_mask[j,:,:])
            
        break
    
    
    
    break


    
    




