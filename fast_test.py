# coding: UTF-8
#特徴量抽出->FAST(高速化はとりあえずなし)

import cv2
import numpy as np
import fast
import time
import process_img

start = time.time()
#画像読み込み
img = cv2.imread('1-005-1.jpg', cv2.IMREAD_GRAYSCALE)
img_raw = cv2.imread('1-005-1.jpg')
img2 = cv2.imread('1-005-2.jpg', cv2.IMREAD_GRAYSCALE)
img_raw2 = cv2.imread('1-005-2.jpg')

#各種変数値
t = 50 #明るさの閾値
n = 12 #周囲の点16点のうち明るさ条件が連続する点の数

#各画像の特徴量の格納用array
img1_feature = []
img2_feature = []

fast1 = fast.FAST(img, t, n)
img1_feature = fast1.get_img_feature()

fast2 = fast.FAST(img2, t, n)
img2_feature = fast2.get_img_feature()

elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

    

crtical_feature_array = []

min_feature1 = (0,0)
min_feature2 = (0,0)
min_diff = 1000000000
for feature1 in img1_feature:
  x1,y1,f1 = feature1
  for feature2 in img2_feature:
    x2,y2,f2 = feature2
    brightness_around_array = np.array(
      [
        int(img[y1-3][x1]),
        int(img[y1-3][x1+1]),
        int(img[y1-2][x1+2]),
        int(img[y1-1][x1+3]),
        int(img[y1][x1+3]),
        int(img[y1+1][x1+3]),
        int(img[y1+2][x1+2]),
        int(img[y1+3][x1+1]),
        int(img[y1+3][x1]),
        int(img[y1+3][x1-1]),
        int(img[y1+2][x1-2]),
        int(img[y1+1][x1-3]),
        int(img[y1][x1-3]),
        int(img[y1-1][x1-3]),
        int(img[y1-2][x1-2]),
        int(img[y1-3][x1-1])
      ]
    )

    brightness_around_array2 = np.array(
      [
        int(img2[y2-3][x2]),
        int(img2[y2-3][x2+1]),
        int(img2[y2-2][x2+2]),
        int(img2[y2-1][x2+3]),
        int(img2[2][x2+3]),
        int(img2[y2+1][x2+3]),
        int(img2[y2+2][x2+2]),
        int(img2[y2+3][x2+1]),
        int(img2[y2+3][x2]),
        int(img2[y2+3][x2-1]),
        int(img2[y2+2][x2-2]),
        int(img2[y2+1][x2-3]),
        int(img2[y2][x2-3]),
        int(img2[y2-1][x2-3]),
        int(img2[y2-2][x2-2]),
        int(img2[y2-3][x2-1])
      ]
    )
    diff = np.sum(np.abs(brightness_around_array-brightness_around_array2))
    if min_diff > diff:
        min_diff = diff
        min_feature1 = (x1,y1)
        min_feature2 = (x2,y2)

height, width = img.shape

width_cors = width - ( min_feature1[0] - min_feature2[0] )
height_cors = height - ( min_feature1[1] - min_feature2[1] ) 


joined_img = process_img.ProcessImg.join_img(img_raw, img_raw2, (width_cors, height_cors))
   
cv2.imshow("result",joined_img)





    
k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite('messigray.png',joined_img)
    cv2.destroyAllWindows()




    
    

