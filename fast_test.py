# coding: UTF-8
#特徴量抽出->FAST(高速化はとりあえずなし)

import cv2
import numpy as np
import fast
import time
import process_img

#測定開始
start = time.time()

#画像読み込み
img1 = cv2.imread('img/1-001-1.jpg')
img2 = cv2.imread('img/1-001-2.jpg')

#各種変数値
t = 50 #明るさの閾値
n = 12 #周囲の点16点のうち明るさ条件が連続する点の数

#各画像の特徴量の格納用array
img1_feature = []
img2_feature = []

fast = fast.FAST(t,n)
img1_feature = fast.get_img_feature(img1)
img2_feature = fast.get_img_feature(img2)

best_feature1, best_feature2 = fast.get_best_match_feature(img1, img1_feature, img2, img2_feature)

joined_img = process_img.ProcessImg.join_img(img1, img2, best_feature1, best_feature2)

cv2.imshow("joined", joined_img)

elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
   
    
k = cv2.waitKey(0)
if k == 27:         
    cv2.destroyAllWindows()
elif k == ord('s'): 
    cv2.imwrite('joined.png',joined_img)
    cv2.destroyAllWindows()




    
    

