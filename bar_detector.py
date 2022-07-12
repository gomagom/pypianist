from line_detector import LineDetector

class BarDetector(LineDetector):
    def __init__(self, img):
        super().__init__(img)


    def detect_bar(self):
        THRESHOLD, DIRECTION = 1.05, 1
        lines = super().extract_lines_coord(self.img, dire=DIRECTION, thresh=THRESHOLD)
        individual_lines = super().merge_serial_lines(lines)

        return individual_lines