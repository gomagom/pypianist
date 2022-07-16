import math
import cv2
import numpy as np
from scipy import ndimage

# 引数で指定した閾値で画像を2値化
def cvt_thresh(img, thresh=128):
    _, result = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)
    return result

# 画像の傾きを補正
def correct_tilt(img, thresh=198):
    img_thresh = cvt_thresh(img, thresh)
    reverse_img = cv2.bitwise_not(img_thresh)
    _, w = img_thresh.shape[:2]
    MIN_LINE_LENGTH = w // 3
    MAX_LINE_GAP = w // 5

    lines = cv2.HoughLinesP(reverse_img, 1, np.pi / 360, 100, MIN_LINE_LENGTH, MAX_LINE_GAP)
    lines = [] if lines is None else lines

    HORIZONTAL = 0  # 基準とする水平線の角度
    DIFF = 10       # 許容誤差 -> -10 - +10 を本来の水平線と考える
    sum_arg = 0
    count = 0
    for line in lines:
        for x1, y1, x2, y2 in line:
            arg = math.degrees(math.atan2((y2 - y1), (x2 - x1)))
            if arg > HORIZONTAL - DIFF and arg < HORIZONTAL + DIFF :
                sum_arg += arg
                count += 1

    ave_arg = (sum_arg / count) - HORIZONTAL if count else HORIZONTAL

    return ndimage.rotate(img, ave_arg, cval = 255)
