from bar_detector import BarDetector
import cv2

class ParagraphDetector:
    def __init__(self, img):
        self.img = img
        self.height, self.width = self.img.shape[:2]

    def detect_para(self, staff):
        para_data = []
        i = 0
        while i < len(staff) - 1:
            top_y = int(staff[i][0]["center"] - (staff[i][0]["weight"] - 1) / 2)
            bottom_y = int(staff[i + 1][-1]["center"] + (staff[i + 1][-1]["weight"] - 1) / 2)
            img_part = self.img[top_y: bottom_y, 0: self.width]
            bar_detector = BarDetector(img_part)
            bar = bar_detector.detect_bar()

            if len(bar) >= 2:
                para_data.append([staff[i], staff[i + 1]])
                i += 1
            else:
                para_data.append([staff[i]])
            i += 1
        if i == len(staff) - 1:
            para_data.append([staff[i]])

        return para_data
