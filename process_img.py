# coding: UTF-8 

import cv2
import numpy as np
import fast

class ProcessImg:

  @classmethod
  def join_img(self, img1, img2, (width_cros,height_cros)):

    #今回はimg1, img2がカラー画像前提
    height1, width1, color1 = img1.shape
    height2, width2, color2 = img2.shape

    #画像処理(tmp系の変数名がダサいのであとで改名)#####################################

    #１枚目の画像に関する処理
    for x in range(width1-width_cros, width1):
      for y in range(height1-height_cros, height1):
        img1[y][x] = [0,0,0]

    zero_row = np.zeros((height2-height_cros,width1,3)).astype(np.uint8)
    img3 = np.concatenate([img1, zero_row],0)
    zero_col = np.zeros((img3.shape[0],width2-width_cros,3)).astype(np.uint8)
    img4 = np.concatenate([img3, zero_col],1)

    #2枚目の画像に関する処理
    zero_row2 = np.zeros((height1-height_cros,width2,3)).astype(np.uint8)
    img5 = np.concatenate([zero_row2, img2],0)
    zero_col2 = np.zeros((img5.shape[0],width1-width_cros,3)).astype(np.uint8)
    img6 = np.concatenate([zero_col2, img5],1)

    ############################################################################

    return img4 + img6

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