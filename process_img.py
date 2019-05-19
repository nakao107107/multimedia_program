# coding: UTF-8 

import cv2
import numpy as np
import fast

class ProcessImg:

  @classmethod
  def join_img(self, img1, img2, img1_feature, img2_feature):

    height1, width1, color1 = img1.shape
    height2, width2, color2 = img2.shape

    x1, y1 = img1_feature
    x2, y2 = img2_feature

    base_img = np.zeros((height1+height2, width1+width2, 3)).astype(np.uint8)
    height,width,color = base_img.shape
    half_width = int(width/2)
    half_height = int(height/2)
    base_img[half_height-y1:half_height+(height1-y1),half_width-x1:half_width+(width1-x1)] = img1
    base_img[half_height-y2:half_height+(height1-y2),half_width-x2:half_width+(width1-x2)] = img2

    return base_img

  @classmethod
  def rotate_img(self, img, angle):
    rotate_matrix = np.array([[np.cos(angle), -np.sin(angle), 0],
                    [np.sin(angle),  np.cos(angle), 0],
                    [        0,          0, 1]])

    H, W, color = img.shape
    WID = int(np.max(img.shape) * 2**0.5)
    e_img = np.zeros((WID, WID, 3)).astype(np.uint8)
    e_img[int((WID-H)/2):int((WID+H)/2),
          int((WID-W)/2):int((WID+W)/2)] = img
    x = np.tile(np.linspace(-1, 1, WID).reshape(1, -1), (WID, 1))
    y = np.tile(np.linspace(-1, 1, WID).reshape(-1, 1), (1, WID))
    p = np.array([[x, y, np.ones(x.shape)]])
    dx, dy, _ = np.sum(p * rotate_matrix.reshape(3, 3, 1, 1), axis=1)
    u = np.clip((dx + 1) * WID / 2, 0, WID-1).astype('i')
    v = np.clip((dy + 1) * WID / 2, 0, WID-1).astype('i')
    return e_img[v, u]


  @classmethod
  def plot_img_feature(self, img, features):

    for feature in features:
      cv2.circle(img, feature, 1, (0, 0, 255), thickness=-1)
    
    return img


  