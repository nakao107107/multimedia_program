import process_img
import cv2
import numpy as np

img_raw = cv2.imread('1-005-1.jpg')
img_result = process_img.ProcessImg.rotate_img(img_raw, np.pi/6)

cv2.imshow("result",img_result)
    
k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite('messigray.png',joined_img)
    cv2.destroyAllWindows()