# coding: UTF-8

import cv2
import numpy as np

class FAST:
  def __init__(self, img, t, n):
    self.img = img
    self.t = t
    self.n = n

  def get_img_feature(self):

    img = self.img
    img_feature= []
    height, width = img.shape

    for x in range(width):
      for y in range(height):

        # #上下左右3ピクセルはアルゴリズムが適用できないのでのぞく
        if x in [0,1,2,width-3,width-2,width-1] or y in [0,1,2,height-3,height-2,height-1]:
            continue

        brightness = self.img[y][x] #基準となる明るさ

        brightness_around_array = np.array(
          [
            int(img[y-3][x]),
            int(img[y-3][x+1]),
            int(img[y-2][x+2]),
            int(img[y-1][x+3]),
            int(img[y][x+3]),
            int(img[y+1][x+3]),
            int(img[y+2][x+2]),
            int(img[y+3][x+1]),
            int(img[y+3][x]),
            int(img[y+3][x-1]),
            int(img[y+2][x-2]),
            int(img[y+1][x-3]),
            int(img[y][x-3]),
            int(img[y-1][x-3]),
            int(img[y-2][x-2]),
            int(img[y-3][x-1])
          ]
        )

        # #現状これがないほうが早く動くんだよなぁ..
        # #高速化プログラム(本来n>12の時適用)#######################################################
        # brightness_status_array = [0,0]

        # for i in [0,4,8,12]:
        #   brightness_status = self.__get_brightness_status(brightness_around_array[i], brightness, self.t)
        #   if brightness_status == "bright":
        #     brightness_status_array[0] += 1 
        #   elif brightness_status == "dark":
        #     brightness_status_array[1] += 1

        #   #明るい点が2点の場合break
        #   if not (brightness_status_array[0]>2 or brightness_status_array[1]>2):
        #     continue
        # ######################################################################################

        sequence_num = 0 #連続する数字
        sequence_num_current = 0 #連続する数字の一時保存領域
        brightness_status ="middle"
        brightness_status_before = "middle"

        #0部分のbrightness statusをここで定義
        brightness_status_before = self.__get_brightness_status(brightness_around_array[0], brightness, self.t)

        #要素数16に対して32回分計算（最初と最後で連番になっていることを考慮）
        for i in range(32):

          #2周目を考慮
          if i >= 16:
            index = i - 16
          else:
            index = i

          #0部分のbrightness statusをここで定義
          brightness_status = self.__get_brightness_status(brightness_around_array[index], brightness, self.t)

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

        if sequence_num > self.n:
          #特徴量を作成
          feature = np.sum(brightness_around_array-brightness)
          print(feature)
          img_feature.append((x,y,feature))

    print("feature detect process finished")
    return img_feature

  #brightness_status取得部分
  def __get_brightness_status (self, target, brightness, t):
    if target > brightness+t:
      return "bright"
    elif target < brightness-t:
      return "dark"
    else:
      return "middle"