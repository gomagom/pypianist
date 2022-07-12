from line_detector import LineDetector
import numpy as np


class StaffDetector(LineDetector):
    def __init__(self, img):
        super().__init__(img)

    
    def detect_staff(self):
        THRESHOLD = 2
        lines = super().extract_lines_coord(self.img, thresh=THRESHOLD)
        individual_lines = super().merge_serial_lines(lines)
        if len(individual_lines) < 5:
            return False, 0 
        grouped_lines, line_pitch = self.grouping_lines(individual_lines)
        staff_lines = self.select_isStaff(grouped_lines)

        for item in grouped_lines:
            if 5 > len(item) > 1 or len(staff_lines) == 0:
                return False, 0

        return staff_lines, line_pitch


    def grouping_lines(self, lines):
        staff_mergin = self.calc_staff_margin(lines)
        groups = []
        line_group = [lines[0]]

        LINE_PITCH_DIFF = 2     # 五線譜の間隔とする基準値からの許容範囲
        for i in range(1, len(lines)):
            if abs(lines[i]["center"] - lines[i - 1]["center"] - staff_mergin) <= LINE_PITCH_DIFF:
                line_group.append(lines[i])
            else:
                groups.append(line_group)
                line_group = [lines[i]]
        groups.append(line_group)

        return groups, staff_mergin

    # 五線譜の線同士の間隔を計算する
    def calc_staff_margin(self, lines):
        mergins = {}
        # 線同士の間隔をキーとする辞書を作成
        # 値は間隔が出現した回数
        for i in range(len(lines) - 1):
            mergin = lines[i + 1]["center"] - lines[i]["center"]
            mergins[mergin] = mergins[mergin] + 1 if mergin in mergins else 1

        # 最頻の間隔の値をndarray化
        staff_mergins = np.array([item[0] for item in mergins.items() if item[1] == max(mergins.values())])

        # 最頻の間隔の値の平均を五線譜の線同士の間隔とする
        return np.mean(staff_mergins)

    
    def select_isStaff(self, grouped_lines):
        return [i for i in grouped_lines if len(i) == 5]

if __name__ == "__main__":
    staff_detector = StaffDetector()
    staff_detector.calc_staff_margin()
