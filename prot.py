import cv2

class Prot:
    def __init__(self) -> None:
        pass


    def export_img(self, imgs):
        for i, img in enumerate(imgs):
            cv2.imwrite('data/dst/img_{:02}.png'.format(i), img)


    def paragraph(self, data, img_thresh):
        img = img_thresh.copy()
        _, w = img.shape[:2]
        self.img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        for idx, item1 in enumerate(data):
            for item2 in item1:
                for item3 in item2:
                    color_list = [(255, 0, 0), (0, 0, 255)]
                    color = color_list[idx % 2]
                    lists = [(item3["center"] - (item3["weight"] - 1) / 2) + i for i in range(item3["weight"])]
                    for y in lists:
                        y = int(y)
                        self.img_rgb = cv2.line(self.img_rgb, (0, y), (w, y), color, 1)

        cv2.imwrite('data/dst/paragraph.png', self.img_rgb)


    def marbles(self, marbles):
        flg = 0
        for i1 in marbles:
            for i2 in i1:
                margin = int(i2[2]) if int(i2[2] % 2) else int(i2[2]) + 1
                flg = 0 if flg else 1
                for j1, j2 in zip(i2[0], i2[1]):
                    color_ = [(0, 255, 255), (255, 255, 0)]
                    for j3 in j2:
                        cv2.ellipse(self.img_rgb, box=((j3, j1[0]), (int(margin * 1), int(margin * 0.6)), 315), color=color_[flg], thickness=-1)

        cv2.imwrite('data/dst/marble.png', self.img_rgb)
