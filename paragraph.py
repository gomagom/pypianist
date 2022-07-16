from staff import Staff
import cv2

class Paragraph:
    def __init__(self, data, no, bar) -> None:
        self.staff_qty = len(data)
        self.no = no
        self.staff = [Staff(item, idx) for idx, item in enumerate(data)]
        self.top = self.staff[0].top
        self.bottom = self.staff[-1].bottom
        self.bar = bar

    # 五線譜を画像から消去
    def remove_staffs(self, img):
        [i.remove_staff(img) for i in self.staff]

    # 小節線を画像から消去
    def remove_bar(self, img):
        for v_line in self.bar:
            cv2.line(img, (int(v_line['center']), int(self.top)-3), (int(v_line['center']), int(self.bottom)+3), 255, v_line['weight']+1)

    # 符頭の位置、種類、音階、順番を検出
    def search_marble_f1(self, img, top_p, bottom_p):
        for idx in range(len(self.staff)):
            top = top_p if idx == 0 else self.staff[idx - 1].bottom
            bottom = bottom_p if idx == len(self.staff) - 1 else self.staff[idx + 1].top
            self.staff[idx].search_marble_f1(img, top, bottom)

    # 小節情報を譜面データに対して追加
    def add_bar_info(self):
        for i in range(len(self.staff)):
            self.staff[i].add_bar_info(self.bar)

    # 全休符情報を譜面データに対して追加
    def add_all_rest_info(self):
        for staff in self.staff:
            for bar in staff.marble_list:
                if bar == []:
                    bar.append([[(), -1, None]])
