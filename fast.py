# coding: UTF-8
import cv2
import numpy as np

class FAST:

  def __init__(self, t, n):
    self.t = t
    self.n = n 

  # カラー画像を引数として、FASTで抽出した特徴点座標をタプルの配列で返す
  def get_img_feature(self, img):

    img_feature= []

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width = img.shape

    for x in range(width):
      for y in range(height):

        #上下左右15ピクセルは処理しない（接合時のことを考慮）
        if (
             x in range(0,15) 
          or x in range(width-15,width) 
          or y in range(0,15) 
          or y in range(height-15,height)
          ):
            continue

        standard_brightness = img[y][x] #基準となる明るさ

        surrounding_pixels = np.array(
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

        consecutive_num_array = [] #明るさ判断が連続して一致した数の格納用
        consecutive_num_el = 0 #明るさ判断が連続して一致した数の一時保存用
        brightness_status = 0
        brightness_status_before = 0

        #0部分のbrightness statusをここで定義
        brightness_status_before = self.__get_brightness_status(surrounding_pixels[0], standard_brightness)

        for i in range(16):

          #0部分のbrightness statusをここで定義
          brightness_status = self.__get_brightness_status(surrounding_pixels[i], standard_brightness)

          #前の要素の明るさが中間値でなく、かつ前の要素と一致する場合
          if brightness_status != 0 and brightness_status_before == brightness_status:

            consecutive_num_el += 1

          else: #前の要素と明るさに関する要件が一致しない

            consecutive_num_array.append(consecutive_num_el)
            consecutive_num_el = 1
          
          #brightness_statusの更新
          brightness_status_before = brightness_status
        
        #最終結果および、最初と最後の足し合わせを末尾に追加
        consecutive_num_array.append(consecutive_num_el)
        consecutive_num_array.append( consecutive_num_array[0] + consecutive_num_array[-1] )

        if np.amax(consecutive_num_array) > self.n:
          img_feature.append((x,y))

    print("feature detect process finished")
    return img_feature


  #２画像とその特徴点からもっともマッチした組み合わせを返す
  #（この関数は回転対応のためにちょっと書き換える必要あり）
  def get_best_match_feature(self, img1, img1_features, img2, img2_features):

    img1_best_feature = (0,0)
    img2_best_feature = (0,0)
    min_diff = 1000000000

    for feature1 in img1_features:

      x1,y1 = feature1

      for feature2 in img2_features:

        x2,y2 = feature2

        img1_fraction = img1[y1-10:y1+10, x1-10:x1+10].astype(np.int8).flatten()
        img2_fraction = img2[y2-10:y2+10, x2-10:x2+10].astype(np.int8).flatten()

        diff = np.sum(np.abs(img1_fraction-img2_fraction))

        if min_diff > diff:
            min_diff = diff
            img1_best_feature = (x1,y1)
            img2_best_feature = (x2,y2)

    return (img1_best_feature, img2_best_feature)

  #brightness_status取得部分
  def __get_brightness_status (self, target, brightness):
    if target > brightness+self.t:
      return 1
    elif target < brightness-self.t:
      return -1
    else:
      return 0