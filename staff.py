import cv2
import numpy as np

class Staff:
    def __init__(self, data, no) -> None:
        self.no = no
        self.staff_lines = data
        self.margin_staff, self._margin_list = self.margin_ave(data)
        self.top = self.staff_lines[0]["center"]
        self.bottom = self.staff_lines[-1]["center"]


    def margin_ave(self, data):
        margin = [data[i + 1]["center"] - data[i]["center"] for i in range(len(data) - 1)]
        margin_ave = sum(margin) / len(margin)
        return margin_ave, margin


    def remove_staff(self, img):
        _, w = img.shape[:2]
        POINT = w // 2
        OVERFLOW = 1
        MIN_LENGTH = w // 140
        middle_x1, middle_x2 = w * 2 // 5, w * 3 // 5
        crop_x1, crop_x2 = POINT - MIN_LENGTH * 4, POINT + MIN_LENGTH * 4
        for item in self.staff_lines:
            lists = []
            right_list = self.search_staff(item, img, POINT, w, MIN_LENGTH)
            left_list = self.search_staff(item, img, POINT, 0, MIN_LENGTH)
            middle_list = self.search_staff(item, img, middle_x1, middle_x2, MIN_LENGTH)

            lists = left_list + right_list
            lists = [i for i in lists if i[0] < crop_x1 or crop_x2 < i[0]]
            middle_list = [i for i in middle_list if crop_x1 <= i[0] <= crop_x2]
            lists.extend(middle_list)

            for item2 in lists:
                top = int(item2[1] - ((item["weight"] - 1) / 2 + OVERFLOW))
                bottom = int(item2[1] + ((item["weight"] - 1) / 2 + OVERFLOW))
                x = item2[0]
                img = cv2.line(img, (x, top), (x, bottom), 255, 1)


    def search_staff(self, data, img, x1, x2, min_length):
        OVERFLOW = 1
        ZONE_WIDTH_PART = int((data["weight"] - 1) / 2 + OVERFLOW)
        LIMIT_MARGIN = 3
        limits = [int(data["center"] - ZONE_WIDTH_PART - LIMIT_MARGIN), int(data["center"] + ZONE_WIDTH_PART + LIMIT_MARGIN)]
        lists = []
        tmp = []

        py = t_py = data["center"]
        for x in range(x1, x2, 1 if x2 - x1 > 0 else -1):
            middle_judge, middle_count = self.judge_alone(img, x, py, ZONE_WIDTH_PART, limits)
            upper_judge, upper_count = self.judge_alone(img, x, py - 1, ZONE_WIDTH_PART, limits)
            lower_judge, lower_count = self.judge_alone(img, x, py + 1, ZONE_WIDTH_PART, limits)

            if not len(tmp):
                t_py = py

            if middle_judge:
                if upper_judge and lower_judge and upper_count > middle_count and lower_count > middle_count:
                    if upper_count > lower_count:
                        py -= 1
                    else:
                        py += 1
                elif upper_judge and upper_count > middle_count:
                    py -= 1
                elif lower_judge and lower_count > middle_count:
                    py += 1
                else:
                    pass
            else:
                if upper_judge and lower_judge:
                    if upper_count > lower_count:
                        py -= 1
                    else:
                        py += 1
                elif upper_judge:
                    py -= 1
                elif lower_judge:
                    py += 1
                else:
                    if len(tmp) > min_length:
                        lists.extend(tmp)
                    else:
                        py = t_py
                    tmp.clear()
                    continue

            tmp.append((x, py))

        if len(tmp) > min_length:
            lists.extend(tmp)

        return lists


    # def remove_bar(self, img):
    #     _, w = img.shape[:2]
    #     POINT = w // 2
    #     OVERFLOW = 1
    #     MIN_LENGTH = w // 140
    #     middle_x1, middle_x2 = w * 2 // 5, w * 3 // 5
    #     crop_x1, crop_x2 = POINT - MIN_LENGTH * 4, POINT + MIN_LENGTH * 4
    #     for item in self.staff_lines:
    #         lists = []
    #         right_list = self.search_staff(item, img, POINT, w, MIN_LENGTH)
    #         left_list = self.search_staff(item, img, POINT, 0, MIN_LENGTH)
    #         middle_list = self.search_staff(item, img, middle_x1, middle_x2, MIN_LENGTH)

    #         lists = left_list + right_list
    #         lists = [i for i in lists if i[0] < crop_x1 or crop_x2 < i[0]]
    #         middle_list = [i for i in middle_list if crop_x1 <= i[0] <= crop_x2]
    #         lists.extend(middle_list)

    #         for item2 in lists:
    #             top = int(item2[1] - ((item[1] - 1) / 2 + OVERFLOW))
    #             bottom = int(item2[1] + ((item[1] - 1) / 2 + OVERFLOW))
    #             x = item2[0]
    #             img = cv2.line(img, (x, top), (x, bottom), 255, 1)


    def judge_alone(self, img, x, py, width, limits):
        top_out = int(py - width - 1)
        bottom_out = int(py + width + 1)
        if top_out >= limits[0] and bottom_out <= limits[1] and img[top_out, x] == 255 and img[bottom_out, x] == 255:
            judge = True
        else:
            judge = False

        count = 0
        basic_point = width + 1
        for i in range(int(py - width), int(py + width + 1)):
            if img[i, x] == 0:
                count += (basic_point - abs(i - py)) * 2

        return judge, count


    def search_marble_f1(self, img, top, bottom):
        scan_y = []
        for idx, item in enumerate(self.staff_lines):
            scan_y.extend([(item["center"], idx * 2), (item["center"] + self.margin_staff / 2, idx * 2 + 1)])
        scan_y.pop(-1)

        scan_y_top = []
        scan_y_bottom = []
        bottom_y = self.bottom
        top_y = self.top
        for i in range(int((bottom - self.bottom - self.margin_staff) // (self.margin_staff / 2))):
            bottom_y += self.margin_staff / 2
            scan_y_bottom.append((bottom_y, i + len(scan_y)))

        for i in range(int((self.top - top - self.margin_staff) // (self.margin_staff / 2))):
            top_y -= self.margin_staff / 2
            scan_y_top.insert(0, (top_y, -i - 1))

        scan_y = scan_y_top + scan_y + scan_y_bottom
        scan_y = [(round(i[0]), i[1]) for i in scan_y]
        
        h, w = img.shape[:2]
        mask_margin_v = int(self.margin_staff) if int(self.margin_staff) % 2 else int(self.margin_staff) + 1
        mask_margin_h = int(self.margin_staff * 1.5) if int(self.margin_staff * 1.5) % 2 else int(self.margin_staff * 1.5) + 1

        # mask_margin -= 2
        mask = np.zeros((mask_margin_v, mask_margin_h), dtype=np.uint8)
        margin_vr = mask_margin_v // 2
        margin_hr = mask_margin_h // 2
        cv2.ellipse(mask, box=((margin_hr, margin_vr), (int(mask_margin_v * 1), int(mask_margin_v * 0.6)), 315), color=255, thickness=-1)
        cv2.imwrite('data/dst/test2.png', mask)

        lists = []
        for y in scan_y:
            lists.append(self.scan_marble_on_horizon(img, w, y[0], y[1], mask, margin_vr, margin_hr))

        return [scan_y, lists, self.margin_staff]


    def scan_marble_on_horizon(self, img, w, y, no, mask, margin_vr, margin_hr):
        list_ = []
        for i in range(margin_hr, w - margin_hr):
            if img[y, i] == 0:
                for j in range(-1, 2):
                    img_p = img[y - margin_vr + j: y + margin_vr + 1 + j, i - margin_hr: i + margin_hr + 1]
                    img_p = img_p & mask
                    if np.count_nonzero(img_p == 255) <= img_p.size // 100 and self.concrete_extend_marble(img, i, no):
                        list_.append(i)
                        break

        return list_


    def concrete_extend_marble(self, img, x, no):
        if 0 <= no <= 8:
            return True 
        diff = (no - 8) // 2 if no > 0 else -no // 2
        pos = self.bottom if no > 0 else self.top
        length = self.margin_staff
        for i in range(diff):
            if no > 0:
                pos += length
            else:
                pos -= length
            img_p = img[round(pos) - 1: round(pos) + 2, x - int(length // 2): x + int(length // 2)]
            flg = False
            for item in img_p:
                flg = True if not np.count_nonzero(item == 255) else flg
            if not flg:
                return False

        return True
