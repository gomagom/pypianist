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

    # 符頭の位置を描画
    def marbles(self, score):
        for paragraph in score.paragraph:
            for staff in paragraph.staff:
                margin = staff.margin_staff
                for bar in staff.marble_list:
                    for i, marble_group in enumerate(bar):
                        if i % 2:
                            marble_color = (0,255,255)
                        else:
                            marble_color = (255, 255, 0)

                        for marble in marble_group:
                            marble_type = marble[1]
                            if marble_type % 2:
                                marble_type -= 1
                                cv2.line(self.img_rgb, (int(marble[0][0]+margin-2), marble[0][1]), (int(marble[0][0]+margin+2), marble[0][1]), (255,0,0), thickness=4)
                            if marble_type <= 2:
                                edge_color = (255, 0, 255)
                            elif marble_type == 4:
                                edge_color = (255, 0, 0)
                            elif marble_type == 8:
                                edge_color = (0, 255, 0)
                            else:
                                edge_color = (0, 0, 255)
                            cv2.ellipse(self.img_rgb, box=((marble[0][0], marble[0][1]), (int(margin * 1.2), int(margin * 0.8)), -30), color=marble_color, thickness=-1)
                            cv2.ellipse(self.img_rgb, box=((marble[0][0], marble[0][1]), (int(margin * 1.2), int(margin * 0.8)), -30), color=edge_color, thickness=2)

                for i, y in enumerate(staff.group_line_y):
                    cv2.line(self.img_rgb, (y[0]-2, y[1]), (y[0]+2, y[1]), (255,0,0), thickness=1)

                    # for j3 in j2:
                    #     if j3[1] <= 2:
                    #         color_ = [(0, 255, 128), (255, 128, 0)]
                    #         cv2.ellipse(self.img_rgb, box=((j3[0], j1[0]), (int(margin * 1.2), int(margin * 0.8)), -30), color=color_[flg], thickness=-1)
                    #     else:
                    #         color_ = [(0, 255, 255), (255, 255, 0)]
                    #         cv2.ellipse(self.img_rgb, box=((j3[0], j1[0]), (int(margin * 1.2), int(margin * 0.8)), -30), color=color_[flg], thickness=-1)

        cv2.imwrite('data/dst/marble.png', self.img_rgb)
