import numpy as np
import wave
import csv
from itertools import groupby
from fractions import Fraction
import sys
import player.music_class as mc

def synthesizer(file_name):
    data = import_data(file_name)
    music = mc.Music(file_name, data)
    y = music.make_music_wave()

    # 量子化
    y = (y*32767).astype(np.int16)
    try:
        with wave.Wave_write("./data/dst/{}.wav".format(file_name)) as fp:
            fp.setframerate(music.sampling_rate)
            fp.setnchannels(1) # モノラル
            fp.setsampwidth(2) # 16ビット（バイト数を入力する）
            fp.writeframes(y.tobytes()) # バイナリ化
    except Exception as e:
        print(e)
        exit(1)

# CSVファイルの読み込み
def import_data(file_name):
    try:
        with open("./data/dst/" + file_name + ".csv", "r", encoding="utf_8") as file:
            reader = csv.reader(file, skipinitialspace=True)
            data = [row for row in reader][1:]
    except FileNotFoundError as e:
        print("ファイルが見つかりません", e)
        exit(1)
    except Exception as e:
        print(e)
        exit(1)

    data.sort(key=lambda x: [int(x[0]), int(x[1])])
    data = [[list(row)[1:] for row in track] for key, track in groupby(data, key=lambda x: x[0])]
    data = [[[list(row)[1:] for row in track] for key, track in groupby(group, key=lambda x: x[0])] for group in data]

    data_t = [[] for i in range(len(data))]
    
    for i, truck in enumerate(data):
        t = Fraction(0)
        for j, unit in enumerate(truck):
            length = Fraction(1, Fraction(unit[0][1]))
            elm = [(note[0], float(note[2])) for note in unit]
            if elm[0][0] != "R":
                data_t[i].append([elm, length, t])
            t += length

    return data_t

# トラックの書式
# [ [ユニット], [ [(単音), (音階, ベロシティ)], 長さ, 距離 ] ]
# [[[("C4", 1)], 1/4, 0], [[("C4", 1), ("E4", 1), ("G4", 1)], 1/4, 1/4], [[("E4", 0.5), ("G4", 0.5), ("B4", 0.5)], 1/8, 1/2]]