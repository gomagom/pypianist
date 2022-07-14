from bar_detector import BarDetector
import cv2

class ParagraphDetector:
    def __init__(self, img):
        self.img = img
        self.height, self.width = self.img.shape[:2]

    def detect_para(self, staff):
        para_data = []
        bar_data = []
        i = 0
        while i < len(staff) - 1:
            top_y = int(staff[i][0]["center"])
            bottom_y = int(staff[i + 1][-1]["center"])
            img_part = self.img[top_y: bottom_y, 0: self.width]
            bar_detector = BarDetector(img_part)
            bar = bar_detector.detect_bar()

            if len(bar) >= 2:
                para_data.append([staff[i], staff[i + 1]])
                bar_data.append(bar)
                i += 1
            else:
                para_data.append([staff[i]])
                bottom_y = int(staff[i][-1]["center"])
                img_part = self.img[top_y: bottom_y, 0: self.width]
                bar_detector = BarDetector(img_part)
                bar = bar_detector.detect_bar()
                bar_data.append(bar)
            i += 1
        if i == len(staff) - 1:
            para_data.append([staff[i]])
            top_y = int(staff[i][0]["center"])
            bottom_y = int(staff[i][-1]["center"])
            img_part = self.img[top_y: bottom_y, 0: self.width]
            bar_detector = BarDetector(img_part)
            bar = bar_detector.detect_bar()
            bar_data.append(bar)

        return para_data, bar_data
