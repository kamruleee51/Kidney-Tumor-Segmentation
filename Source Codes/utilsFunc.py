# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 22:50:01 2019

@author: kamrul
"""

from pathlib import Path

import nibabel as nib

import numpy as np

from skimage import data, color, io, img_as_float


def get_full_case_id(cid):
    #cid is the integer of the image name
    try:
        cid = int(cid)
        case_id = "case_{:05d}".format(cid)
    except ValueError:
        case_id = cid

    return case_id

def get_case_path(cid):
    # Resolve location where data should be living
    data_path = Path(__file__).parent.parent / "scripts/dataTrain/"
#    print(data_path)
    if not data_path.exists():
        raise IOError(
            "Data path, {}, could not be resolved".format(str(data_path))
        )

    # Get case_id from provided cid
    case_id = get_full_case_id(cid)

    # Make sure that case_id exists under the data_path
    case_path = data_path / case_id
    if not case_path.exists():
        raise ValueError(
            "Case could not be found \"{}\"".format(case_path.name)
        )

    return case_path

def load_volume(cid):
    case_path = get_case_path(cid)
    vol = nib.load(str(case_path / "imaging.nii.gz"))
    return vol


def load_segmentation(cid):
    case_path = get_case_path(cid)
    seg = nib.load(str(case_path / "segmentation.nii.gz"))
    return seg


def load_case(cid):
    vol = load_volume(cid)
    seg = load_segmentation(cid)
    return vol, seg


def mask_overlay_org (org,mask):
    
    mask_tumor = mask.copy()
    mask_kidney = mask.copy()
    
    mask_kidney[mask_kidney!=1]=0
    mask_kidney[mask_kidney==1]=255
    
    mask_tumor[mask_tumor!=2]=0
    mask_tumor[mask_tumor==2]=255
    
    img_color = np.dstack((org, org, org))
    
    kidney_color = np.zeros_like(img_color)
    kidney_color[mask_kidney!=0] = [0, 0, 255] # Blue block
        
    tumor_color = np.zeros_like(img_color)
    tumor_color[mask_tumor!=0] = [0, 255, 0] # Blue block
        
    tumor_overlay = color.rgb2hsv(img_color)
    kidney_overlay = tumor_overlay.copy()
    
    kidney_color = color.rgb2hsv(kidney_color)
    tumor_color = color.rgb2hsv(tumor_color)
        
    kidney_overlay[:,:, 0] = kidney_color[:,:, 0]
    kidney_overlay[:,:, 1] = kidney_color[:,:, 1] * 0.6
    kidney_overlay = color.hsv2rgb(kidney_overlay)
    
    tumor_overlay[:,:, 0] = tumor_color[:,:, 0]
    tumor_overlay[:,:, 1] = tumor_color[:,:, 1] * 0.6
    tumor_overlay = color.hsv2rgb(tumor_overlay)
    
    return kidney_overlay, tumor_overlay