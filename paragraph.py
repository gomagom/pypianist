from staff import Staff

class Paragraph:
    def __init__(self, data, no) -> None:
        self.staff_qty = len(data)
        self.no = no
        self.staff = [Staff(item, idx) for idx, item in enumerate(data)]
        self.top = self.staff[0].top
        self.bottom = self.staff[-1].bottom


    def remove_staffs(self, img):
        [i.remove_staff(img) for i in self.staff]


    def search_marble_f1(self, img, top_p, bottom_p):
        result = []
        for idx, item in enumerate(self.staff):
            top = top_p if idx == 0 else self.staff[idx - 1].bottom
            bottom = bottom_p if idx == len(self.staff) - 1 else self.staff[idx + 1].top
            result.append(item.search_marble_f1(img, top, bottom))

        return result
