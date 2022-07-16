from numpy import shape
import pandas as pd

# 音の長さを4/4拍子中の割合として分数で計算し、その逆数を返却(見やすさのため)
def calc_length(note_type):
    if note_type < 0:
        return ["R", str(-note_type)]
    with_dot = False
    if note_type > 1 and note_type % 2:
        with_dot = True
        note_type -= 1

    if with_dot:
        note_length = str(note_type * 2) + "/3"
    else:
        note_length = str(note_type)

    return note_length


# 音階を計算し、国際式に変換して返却
def calc_degree(position_num, upper=True):
    # position_num … 第5線を0として、1度低くなる毎に+1、高くなる毎に-1している
    keys = ["B", "A", "G", "F", "E", "D", "C"]
    if upper:
        move_num = 3
        base_octave = 5
    else:
        move_num = 1
        base_octave = 3

    # オクターブ内に合わせるため、番号をずらす
    position_num_mod = position_num + move_num
    key = keys[position_num_mod % 7]
    octave = base_octave - (position_num_mod // 7)

    return key + str(octave)

# 譜面データをCSVに出力する形式に変換する
def data_shaping(score):
    score_data = []
    velocity = 1
    track_qty = len(score.paragraph[0].staff)
    for track in range(track_qty):
        upper = True if track == 0 else False
        unit_num = 0
        for paragraph in score.paragraph:
            source_list = paragraph.staff[track].marble_list
            for bar in source_list:
                for group in bar:
                    for note in group:
                        length = calc_length(note[1])
                        if type(length) == list:
                            score_data.append([track, unit_num, length[0], length[1], velocity])
                            break
                        degree = calc_degree(note[2], upper)
                        score_data.append([track, unit_num, degree, length, velocity])
                    unit_num += 1

    return score_data

# csv形式で譜面を出力
def export_csv(score, path):
    shaped_score_data = data_shaping(score)
    score_df = pd.DataFrame(shaped_score_data, columns=['トラック', 'ユニット', '音階', '長さ', 'ベロシティ'])
    score_df.to_csv("./data/dst/" + path + ".csv", index=False)
