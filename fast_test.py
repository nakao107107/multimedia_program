# coding: UTF-8
#特徴量抽出->FAST(高速化はとりあえずなし)

import cv2
import numpy as np
import time

start = time.time()

#画像読み込み
img = cv2.imread('1-001-1.jpg', cv2.IMREAD_GRAYSCALE)
img_raw = cv2.imread('1-001-1.jpg')
img2 = cv2.imread('1-001-2.jpg', cv2.IMREAD_GRAYSCALE)
img_raw2 = cv2.imread('1-001-2.jpg')

#各種変数値
t = 50 #明るさの閾値
n = 12 #周囲の点16点のうち明るさ条件が連続する点の数

#各画像の特徴量の格納用array
img1_feature = []
img2_feature = []

#brightness_status取得部分関数化（多分あとで全体をclass化する）
def get_brightness_status (target, brighness, t):
  if target > brightness+t:
    return "bright"
  elif target < brightness-t:
    return "dark"
  else:
    return "middle"

# #１枚目の画像に関する処理
height, width = img.shape

for x in range(width):
  for y in range(height):

    # #上下左右3ピクセルはアルゴリズムが適用できないのでのぞく
    if x in [0,1,2,317,318,319] or y in [0,1,2,237,238,239]:
        continue

    brightness = img[y][x] #基準となる明るさ

    brightness_around_array = np.array(
      [
        img[y-3][x],
        img[y-3][x+1],
        img[y-2][x+2],
        img[y-1][x+3],
        img[y][x+3],
        img[y+1][x+3],
        img[y+2][x+2],
        img[y+3][x+1],
        img[y+3][x],
        img[y+3][x-1],
        img[y+2][x-2],
        img[y+1][x-3],
        img[y][x-3],
        img[y-1][x-3],
        img[y-2][x-2],
        img[y-3][x-1]
      ]
    )

    #高速化プログラム(本来n>12の時適用)#######################################################
    brightness_status_array = [0,0]

    for i in [0,4,8,12]:
      brightness_status = get_brightness_status(brightness_around_array[i], brightness, t)
      if brightness_status == "bright":
        brightness_status_array[0] += 1 
      elif brightness_status == "dark":
        brightness_status_array[1] += 1

      #明るい点が2点の場合break
      if not (brightness_status_array[0]>2 or brightness_status_array[1]>2):
        continue
    ######################################################################################

    sequence_num = 0 #連続する数字
    sequence_num_current = 0 #連続する数字の一時保存領域
    brightness_status ="middle"
    brightness_status_before = "middle"

    #0部分のbrightness statusをここで定義(あとで関数化)
    brightness_status_before = get_brightness_status(brightness_around_array[0], brightness, t)

    #要素数16に対して32回分計算（最初と最後で連番になっていることを考慮）
    for i in range(32):

      #2周目を考慮
      if i >= 16:
        index = i - 16
      else:
        index = i

      #0部分のbrightness statusをここで定義(あとで関数化)
      brightness_status = get_brightness_status(brightness_around_array[index], brightness, t)

      #前の要素の明るさが中間値でなく、かつ前の要素と一致する場合
      if brightness_status != "middle" and brightness_status_before == brightness_status:
        sequence_num_current += 1

      else: #前の要素と明るさに関する要件が一致しない

        #sequence_numが最大値の場合はsequence_numに移してからリセット
        if sequence_num_current > sequence_num:
          sequence_num = sequence_num_current
          
        sequence_num_current = 1
      
      #brightness_statusの更新
      brightness_status_before = brightness_status

    if sequence_num > n:
      cv2.circle(img_raw, (x,y), 1, (255, 0, 0), thickness=1, lineType=cv2.LINE_8, shift=0)
      img1_feature.append((x,y))

print("process1 finished")

#非最大値抑制を入れる

elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")


cv2.imshow("result1", img_raw)

k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite('messigray.png',img_raw)
    cv2.destroyAllWindows()




    
    

