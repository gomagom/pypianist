import cv2
import numpy as np
class Marble:
    def __init__(self, img):
        self.img = img
        self.height, self.width = self.img.shape[:2]
        self.img_size = self.height * self.width

    def find_object(self):
        result_img = cv2.cvtColor(self.img, cv2.COLOR_GRAY2RGB)
        contours, hierarchy = cv2.findContours(self.img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # 特徴量検出機を作成
        detector = cv2.AKAZE_create() 
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = False)

        toon_img = cv2.cvtColor(cv2.imread("./data/model/m138.png"), cv2.COLOR_BGR2GRAY)
        _, toon = detector.detectAndCompute(cv2.cvtColor(cv2.imread("./data/model/m78.png"), cv2.COLOR_BGR2GRAY), None)


        for i, contour in enumerate(contours):
            # 小さな領域の場合は間引く
            area = cv2.contourArea(contour)
            if area < 50:
                continue
            # 画像全体を占める領域は除外する
            if self.img_size * 0.99 < area:
                continue
            # 外接矩形を取得
            x,y,w,h = cv2.boundingRect(contour)
            if w < 10 or h < 10:
                continue
            # 外接矩形で囲まれた箇所のイメージを切り出し
            cut = self.img[y:y+h, x:x+w]
            height = 512
            width = round(w * (height / h))
            cut = cv2.resize(cut, dsize=(width, height), interpolation=cv2.INTER_CUBIC)
            retval, cut = cv2.threshold(cut, 128, 255, cv2.THRESH_BINARY)
            # cv2.imwrite(f'data/model/m{i}.png', cut)
            _, des_orb = detector.detectAndCompute(cut, None)
            # 特徴量検出機を作成し解析
            matches = matcher.match(des_orb, toon)
            dist = [m.distance for m in matches]
            # 差の平均
            if len(dist) == 0:
                continue
            ret = sum(dist) / len(dist)
            print(ret)
            # 少ないほど一致
            if ret < 40:
                result_img = cv2.rectangle(result_img, (x, y), (x + w, y + h), (255, 0, 0), 3)
            else:
                result_img = cv2.rectangle(result_img, (x, y), (x + w, y + h), (0, 255, 0), 3)


        return result_img


if __name__ == "__main__":
    PATH = "./data/dst/test.png"
    img = cv2.cvtColor(cv2.imread(PATH), cv2.COLOR_BGR2GRAY)
    marble = Marble(img)
    result_img = marble.find_object()
    cv2.imwrite('data/dst/test3.png', result_img)
