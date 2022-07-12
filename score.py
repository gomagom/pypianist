from image_manager import *
from staff_detector import StaffDetector
from paragraph_detector import ParagraphDetector
from paragraph import Paragraph
import cv2


class Score:
    def __init__(self, path):
        self.path = path
        self.img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)
        self.img = correct_tilt(self.img)
        self.height, self.width = self.img.shape[:2]
        self.img_thresh_base = cvt_thresh(self.img)
        self.paragraph = []

    def detect_lines(self):
        thresh_current = 128
        STEP = 16
        while thresh_current < 255:
            staff_detector = StaffDetector(self.img_thresh_base)
            staff_list, pitch = staff_detector.detect_staff()
            if staff_list:
                break
            thresh_current += STEP
            self.img_thresh_base = cvt_thresh(self.img, thresh_current)
        else:
            print("五線譜を正しく読み取れません")
            exit(1)

        para_detector = ParagraphDetector(self.img_thresh_base)
        paragraph = para_detector.detect_para(staff_list)
        self.paragraph = [Paragraph(item, idx) for idx, item in enumerate(paragraph)]

        return paragraph, pitch


    def labeling(self, pitch):
        self._img2 = self.img_thresh_base.copy()
        # map(lambda i: i.remove_staffs(self._img2), self._paragraph)
        [i.remove_staffs(self._img2) for i in self.paragraph]

        # テスト用出力
        cv2.imwrite('data/dst/test.png', self._img2)

        self._img3 = self._img2.copy()
        result = []
        for idx, item in enumerate(self.paragraph):
            top = 0 if idx == 0 else self.paragraph[idx - 1].bottom
            bottom = self.height if idx == len(self.paragraph) - 1 else self.paragraph[idx + 1].top
            result.append(item.search_marble_f1(self._img3, top, bottom))
        return result
