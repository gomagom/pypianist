import cv2
import numpy as np

class Staff:
    def __init__(self, data, no) -> None:
        self.no = no
        self.staff_lines = data
        self.margin_staff, self._margin_list = self.margin_ave(data)
        self.top = self.staff_lines[0]["center"]
        self.bottom = self.staff_lines[-1]["center"]
        self.marble_list = []
        self.group_line_y = []

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
        cv2.ellipse(mask, box=((margin_hr, margin_vr), (int(mask_margin_v * 1.2), int(mask_margin_v * 0.8)), -30), color=255, thickness=-1)
        mask_circle = mask.copy()
        cv2.ellipse(mask_circle, box=((margin_hr, margin_vr), (int(mask_margin_v * 1.2), int(mask_margin_v * 0.5)), -40), color=0, thickness=-1)
        mask_circle_center = np.zeros((mask_margin_v, mask_margin_h), dtype=np.uint8)
        cv2.ellipse(mask_circle_center, box=((margin_hr, margin_vr), (int(mask_margin_v * 1), int(mask_margin_v * 0.4)), -40), color=255, thickness=-1)
        mask_circle_center = cv2.line(mask_circle_center, (0, margin_hr // 2), (margin_vr, margin_hr // 2), 0, 1)
        cv2.imwrite('data/dst/test2.png', mask)
        cv2.imwrite('data/dst/test4.png', mask_circle)

        marbles_on_staff = []
        for y in scan_y:
            marbles_on_staff.extend(self.scan_marble_on_horizon(img, w, int(y[0]), int(y[1]), mask, mask_circle, mask_circle_center, margin_vr, margin_hr))

        self.marble_list = marbles_on_staff
        self.grouping_marble()
        self.judge_marble_type(img)
        print(self.marble_list)
        # return [scan_y, marbles_on_staff, self.margin_staff]

    def scan_marble_on_horizon(self, img, w, y, no, mask, mask_circle, mask_circle_center, margin_vr, margin_hr):
        list_marble = []
        # i = margin_hr
        # while i < w - margin_hr:
        for i in range(margin_hr, w - margin_hr):
            if img.item(y, i) == 0:
                for j in range(-2, 3):
                    img_p = img[y - margin_vr + j: y + margin_vr + 1 + j, i - margin_hr: i + margin_hr + 1]
                    img_judge = img_p & mask
                    if np.count_nonzero(img_judge == 255) <= img_judge.size // 100 and self.concrete_extend_marble(img, i, no):
                        list_marble.append([(i, y), 4, no])
                        break
                    else:
                        img_judge = img_p & mask_circle
                        img_judge2 = cv2.bitwise_not(img_p) & mask_circle_center
                        if np.count_nonzero(img_judge == 255) <= img_judge.size // 100 and np.count_nonzero(img_judge2 == 255) <= img_judge2.size // 10 and self.concrete_extend_marble(img, i, no):
                            list_marble.append([(i, y), 2, no])
                            break
            else:
                for j in range(-2, 3):
                    img_p = img[y - margin_vr + j: y + margin_vr + 1 + j, i - margin_hr: i + margin_hr + 1]
                    img_judge = img_p & mask_circle
                    img_judge2 = cv2.bitwise_not(img_p) & mask_circle_center
                    if np.count_nonzero(img_judge == 255) <= img_judge.size // 100 and np.count_nonzero(img_judge2 == 255) <= img_judge2.size // 10 and self.concrete_extend_marble(img, i, no):
                        list_marble.append([(i, y), 2, no])
                        break

        list_marble = self.combine_duplicate_marble(list_marble, margin_vr)

        return list_marble


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
            img_p = img[int(round(pos)) - 1: int(round(pos)) + 2, x - int(length // 2): x + int(length // 2)]
            flg = False
            for item in img_p:
                flg = True if not np.count_nonzero(item == 255) else flg
            if not flg:
                return False

        return True

    def combine_duplicate_marble(self, marble_list, margin_vr):
        duplicate_list = []
        result_list = []
        for item in marble_list:
            if duplicate_list == []:
                duplicate_list.append(item)
                continue
            if item[0][0] - duplicate_list[-1][0][0] < margin_vr:
                duplicate_list.append(item)
            else:
                result_list.append(self.find_max_type(duplicate_list))
                duplicate_list = []
        if len(duplicate_list) > 0:
            result_list.append(self.find_max_type(duplicate_list))

        return result_list

    def find_max_type(self, duplicate_list):
        type_max = 2
        for item in duplicate_list:
            if item[1] > 2:
                type_max = item[1]

        return [duplicate_list[len(duplicate_list) // 2][0], type_max, duplicate_list[len(duplicate_list) // 2][2]]

    # 同時に鳴る音符をグループ化(縦に並んでいる玉をまとめる)
    def grouping_marble(self):
        grouped_marbel_list = []
        thresh = self.margin_staff * 1.5
        while self.marble_list:
            top_marble = self.marble_list.pop(0)
            group = [top_marble]
            group_idx = []
            for i, marble in enumerate(self.marble_list):
                if abs(top_marble[0][0] - marble[0][0]) <= thresh:
                    group.append(marble)
                    group_idx.append(i)
            self.marble_list = [item for idx, item in enumerate(self.marble_list) if idx not in group_idx]
            grouped_marbel_list.append(group)

        grouped_marbel_list = sorted(grouped_marbel_list, key=lambda x: x[0][0])
        self.marble_list = grouped_marbel_list

    def judge_marble_type(self, img):
        judge_area_width = int(self.margin_staff * 1.5)
        judge_area_height = int(self.margin_staff * 1.5)
        marble_type = [4, 8, 16]
        for i, group in enumerate(self.marble_list):
            direction = -1
            top_marble = group[0]
            if top_marble[1] <= 2:
                continue
            start_x = top_marble[0][0] - judge_area_width // 2
            start_y = top_marble[0][1] - int(self.margin_staff // 2) - judge_area_height
            cut = img[start_y:start_y+judge_area_height, start_x:start_x+judge_area_width]
            line_list = self.find_marble_line(cut, start_x)
            if line_list == []:
                direction = 1
                bottom_marble = group[-1]
                start_y = bottom_marble[0][1] + int(self.margin_staff // 2)
                cut = img[start_y:start_y+judge_area_height, start_x:start_x+judge_area_width]
                line_list = self.find_marble_line(cut, start_x)
                if not line_list:
                    return

            line_edge_y = self.calc_marble_line_edge_y(img, line_list, start_y, direction)
            self.group_line_y.append((line_list[len(line_list) // 2], line_edge_y))
            marble_flag_num = self.check_marble_flag(img, line_list, line_edge_y, direction)
            for j in range(len(group)):
                self.marble_list[i][j][1] = marble_type[marble_flag_num]

    def find_marble_line(self, img_cut, x):
        result = []
        h, w = img_cut.shape[:2]
        for i in range(w):
            part = img_cut[0:h, i:i+1]
            if np.size(part) - np.count_nonzero(part) > np.size(part) * 9 / 10:
                result.append(x + i)

        return result

    def calc_marble_line_edge_y(self, img, line_list, y, direction=1):
        start_line_x = line_list[0]
        line_edge_y = y
        while True:
            next_y = line_edge_y + direction
            cut = img[next_y:next_y+1, start_line_x:start_line_x+len(line_list)]
            if np.count_nonzero(cut) == np.size(cut):
                break
            line_edge_y += direction
        
        return line_edge_y

    def check_marble_flag(self, img, line_list, line_edge_y, direction=1):
        zone_height = int(self.margin_staff * 2)
        lines_pair = [line_list[0] - 3, line_list[-1] + 3]
        if direction == 1:
            zone_start_y = line_edge_y - int(self.margin_staff * 1.5)
        else:
            zone_start_y = line_edge_y - int(self.margin_staff // 2)
        check_zone = [img[zone_start_y:zone_start_y+zone_height, lines_pair[0]:lines_pair[0]+1], img[zone_start_y:zone_start_y+zone_height, lines_pair[1]:lines_pair[1]+1]]

        count_max = 0
        for zone in check_zone:
            combo = 0
            count = 0
            for dot in zone:
                if dot[0] == 0:
                    combo += 1
                else:
                    combo = 0
                if combo == int(self.margin_staff // 6):
                    count += 1

            if count_max < count:
                count_max = count

        return count_max

