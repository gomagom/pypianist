import cv2
import numpy as np

class LineDetector:
    def __init__(self, img):
        self.img = img.copy()

    # 画像中から引数で指定した長さ以上の線を検出し、その座標を求める
    def extract_lines_coord(self, img, dire=0, thresh=2):
        if dire == 1:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        h, w = img.shape[:2]
        
        line_list = []
        for r in range(h):
            line_list.append(self.count_dot_series(img, r, w))

        # テスト用出力
        if dire == 0:
            blank = np.zeros((h, w, 3))
            blank += 255
            for i, item in enumerate(line_list):
                cv2.line(blank, (0, i), (item, i), (0,0,255), thickness=1)
            cv2.imwrite('./data/dst/run-length.png', blank)

        # 線の長さが画像の幅の半分以上であれば取得したい線とし、その座標をリストにまとめる
        coord_list = [index for index, item in enumerate(line_list) if item >= w // thresh]

        return coord_list

    # 引数で指定した範囲で横方向にピクセルが連続している最大の数をカウント
    # つまり、範囲中で最も長い横線の長さを返す
    def count_dot_series(self, img, y, width):
        max = count = gap = 0
        MAX_GAP = 6

        for x in range(width):
            if img.item(y, x) == 0:
                count += 1 + gap
                gap = 0
                if count > max:
                    max = count
            else:
                gap += 1

            if gap > MAX_GAP:
                count = gap = 0

        return max

    # 隣接する線を1本の線としてまとめ、線を(中心の座標, 幅)とする
    def merge_serial_lines(self, lines):
        individual_lines = []
        line_group = []
        for i, item in enumerate(lines):
            line_group.append(item)
            if i == len(lines) - 1 or item + 1 != lines[i + 1]:
                center = np.mean(line_group)
                weight = len(line_group)
                individual_lines.append({"center": center, "weight": weight})
                line_group.clear()

        return individual_lines
