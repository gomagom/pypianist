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


    def remove_staffs(self, img):
        [i.remove_staff(img) for i in self.staff]

    def remove_bar(self, img):
        for v_line in self.bar:
            cv2.line(img, (int(v_line['center']), int(self.top)-3), (int(v_line['center']), int(self.bottom)+3), 255, v_line['weight'])


    def search_marble_f1(self, img, top_p, bottom_p):
        for idx in range(len(self.staff)):
            top = top_p if idx == 0 else self.staff[idx - 1].bottom
            bottom = bottom_p if idx == len(self.staff) - 1 else self.staff[idx + 1].top
            self.staff[idx].search_marble_f1(img, top, bottom)
            self.staff[idx].add_bar_info(self.bar)
            print(self.staff[idx].marble_list)
