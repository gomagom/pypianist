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

        for i, contour in enumerate(contours):
            # 小さな領域の場合は間引く
            area = cv2.contourArea(contour)
            if area < 500:
                continue
            # 画像全体を占める領域は除外する
            if self.img_size * 0.99 < area:
                continue
            # 外接矩形を取得
            x,y,w,h = cv2.boundingRect(contour)
            # 外接矩形で囲まれた箇所のイメージを切り出し
            result_img = cv2.rectangle(result_img, (x, y), (x + w, y + h), (0, 255, 0), 3)

        return result_img


# img = cv2.imread("./data/model/kyufu1.png", -1)
# # αチャンネルが0となるインデックスを取得
# # ex) ([0, 1, 3, 3, ...],[2, 4, 55, 66, ...])
# # columnとrowがそれぞれ格納されたタプル(長さ２)となっている
# index = np.where(img[:, :, 3] == 0)
# # 白塗りする
# img[index] = [255, 255, 255, 255]
# # 出力
# cv2.imwrite("data/model/4-kyufu.png", img)
if __name__ == "__main__":
    PATH = "./data/model/4-kyufu.png"
    img = cv2.cvtColor(cv2.imread(PATH), cv2.COLOR_BGR2GRAY)
    # しきい値指定によるフィルタリング
    retval, dst = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    cv2.imwrite('data/model/4-kyufu.png', dst)
