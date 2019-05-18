# coding: UTF-8
#特徴量抽出->FAST(高速化はとりあえずなし)

import cv2
import numpy as np
import fast
import time
import process_img

start = time.time()
#画像読み込み
img = cv2.imread('1-002-1.jpg', cv2.IMREAD_GRAYSCALE)
img_raw = cv2.imread('1-002-1.jpg')
img2 = cv2.imread('1-002-2.jpg', cv2.IMREAD_GRAYSCALE)
img_raw2 = cv2.imread('1-002-2.jpg')

#各種変数値
t = 50 #明るさの閾値
n = 12 #周囲の点16点のうち明るさ条件が連続する点の数

#各画像の特徴量の格納用array
img1_feature = []
img2_feature = []

fast = fast.FAST()
img1_feature = fast.get_img_feature(img, t, n)
img2_feature = fast.get_img_feature(img2, t, n)


elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")


best_feature1 = (0,0)
best_feature2 = (0,0)
min_diff = 1000000000

for feature1 in img1_feature:

  x1,y1 = feature1

  for feature2 in img2_feature:

    x2,y2 = feature2

    around_array = img_raw[y1-10:y1+10, x1-10:x1+10]
    around_array2 = img_raw2[y2-10:y2+10, x2-10:x2+10]

    around_array = around_array.astype(np.int8).flatten()
    around_array2 = around_array2.astype(np.int8).flatten()

    diff = np.sum(np.abs(around_array-around_array2))

    if min_diff > diff:
        min_diff = diff
        best_feature1 = (x1,y1)
        best_feature2 = (x2,y2)


height, width = img.shape

width_cors = width - ( best_feature1[0] - best_feature2[0] )
height_cors = height - ( best_feature1[1] - best_feature2[1] ) 

print(min_diff)
print(best_feature1)
print(best_feature2)


joined_img = process_img.ProcessImg.join_img(img_raw, img_raw2, best_feature1, best_feature2)

img_raw = process_img.ProcessImg.plot_img_feature(img_raw, img1_feature)
img_raw2 = process_img.ProcessImg.plot_img_feature(img_raw2, img2_feature)

cv2.imshow("result1",img_raw)
cv2.imshow("result2",img_raw2)

cv2.imshow("joined", joined_img)
   
    
k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite('messigray.png',joined_img)
    cv2.destroyAllWindows()




    
    

