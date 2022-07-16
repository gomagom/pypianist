import tensorflow.keras
import numpy as np
from tensorflow.keras.models import load_model
import cv2
import os
import warnings
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# 画像中から休符の候補を抽出
def find_rest(img, score):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    target_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        _, y, w, h = cv2.boundingRect(contour)
        center_y = y + h // 2
        for paragraph in score.paragraph:
            for staff in paragraph.staff:
                top = staff.top
                bottom = staff.bottom
                middle = top + (bottom - top) // 2
                margin = staff.margin_staff
                center_diff = abs(middle - center_y)
                # 五線譜上にあり、領域の大きさや形が休符のそれに近いものを選択
                if top <= y and y+h <= bottom and center_diff <= margin // 2 and (margin ** 2) * 4 >= area >= (margin ** 2) * 0.5 and w <= margin * 2:
                    target_contours.append([contour, paragraph.no, staff.no])
    
    # テスト用出力
    result_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    for i, contour in enumerate(target_contours):
        x, y, w, h = cv2.boundingRect(contour[0])
        part_img = result_img[y:y+h, x:x+w]
        cv2.imwrite('data/train/img_{:02}.png'.format(i), part_img)
        result_img = cv2.rectangle(result_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imwrite('data/dst/test3.png', result_img)

    return target_contours

# 休符の判定
def judge_rest_type(img, train_data):
    img1 = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    part_img = img[1:-1, 1:-1]
    if np.count_nonzero(part_img) < np.size(part_img) / 10:
        return -2
    warnings.simplefilter('ignore')
    model = load_model(train_data)
    img_resize = cv2.resize(img1, (50, 100))
    img2 = np.asarray(img_resize)
    img2 = img2 / 255.0
    prd = model.predict(np.array([img2]))
    #print(prd)  # 精度の表示
    prelabel = np.argmax(prd, axis=1)
    if np.max(prd) < 0.7:
        #print("none")
        return 0
    if prelabel == 0:
        #print(">>8kyu")
        return -8
    elif prelabel == 1:
        #print(">4kyu")
        return -4
    else:
        return 0

# 休符情報の返却
def generate_rest_info(score):
    img = score.img_line_removed
    rest_list = []
    target_contours = find_rest(img, score)
    train_data = "./train_data/train_cnn_note.h5"
    for contour in target_contours:
        x, y, w, h = cv2.boundingRect(contour[0])
        coord_x = x + w // 2
        part_img = img[y:y+h, x:x+w]
        rest_type = judge_rest_type(part_img, train_data)
        if rest_type != 0:
            rest_list.append([rest_type, contour[1], contour[2], coord_x])
    
    return rest_list

# 休符情報を既存の符頭データに追加
def insert_rest_info(score):
    rest_list = generate_rest_info(score)
    for rest in rest_list:
        target_staff = score.paragraph[rest[1]].staff[rest[2]]
        marble_list = target_staff.marble_list
        middle_y = int(target_staff.top + (target_staff.bottom - target_staff.top) // 2)
        for i, group in enumerate(marble_list):
            if group[0][0][0] > rest[3]:
                insert_info = [[(rest[3], middle_y), rest[0], None]]
                marble_list.insert(i, insert_info)
                break

