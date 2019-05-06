# coding: UTF-8 

import cv2
import numpy as np
import fast

width_cros = 170
height_cros = 210

img = cv2.imread('1-001-1.jpg', cv2.IMREAD_GRAYSCALE)
img_raw = cv2.imread('1-001-1.jpg')
img2 = cv2.imread('1-001-2.jpg', cv2.IMREAD_GRAYSCALE)
img_raw2 = cv2.imread('1-001-2.jpg')


height1, width1, color1 = img_raw.shape
height2, width2, color2 = img_raw.shape


#１枚目の画像に関する処理
for x in range(width1-width_cros, width1):
  for y in range(height1-height_cros, height1):
    img_raw[y][x] = [0,0,0]

zero_row = np.zeros((height2-height_cros,width1,3)).astype(np.uint8)
img3 = np.concatenate([img_raw, zero_row],0)
zero_col = np.zeros((img3.shape[0],width2-width_cros,3)).astype(np.uint8)
img4 = np.concatenate([img3, zero_col],1)

#2枚目の画像に関する処理
zero_row2 = np.zeros((height1-height_cros,width2,3)).astype(np.uint8)
img5 = np.concatenate([zero_row2, img_raw2],0)
zero_col2 = np.zeros((img5.shape[0],width1-width_cros,3)).astype(np.uint8)
img6 = np.concatenate([zero_col2, img5],1)


img7 = img4+img6

cv2.imshow("result2",img4)
cv2.imshow("result3",img6)
cv2.imshow("result4",img7)
    
k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite('messigray2.png',img7)
    cv2.destroyAllWindows()