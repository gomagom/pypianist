import numpy as np
import math
import configparser as cp
import os
import shutil

import player.sdwave as sw

class Music():
    def __init__(self, name, data):
        self.sampling_rate = 44100
        self.name = name
        self.track = []
        self.import_settings(name)
        for idx, item in enumerate(data):
            # トラックのインスタンスをリストとして保持
            self.track.append(Track(name, idx, item))

    # iniファイルから設定をインポートし、インスタンス変数に格納
    def import_settings(self, name):
        inifile_path = "./data/settings/" + name + ".ini"
        if not os.path.exists(inifile_path):
            shutil.copy("./data/default/default.ini", inifile_path)
        inifile = cp.SafeConfigParser()
        inifile.read(inifile_path)
        try:
            settings = inifile["body"]
        except KeyError as e:
            print(e)
            exit(1)
        except Exception as e:
            print(e)
            exit(1)

        self.bpm = float(settings.get("bpm"))
        self.volume = float(settings.get("volume"))

    # 楽曲の波形を作成
    def make_music_wave(self):
        y = []
        for i in range(len(self.track)):
            y.append(self.track[i].gen_track(self.sampling_rate, self.bpm))
        y = sw.synthesize_wave(y) * self.volume

        # 曲の最後より後ろをカット
        can = np.where(y != 0)[0][-1]
        point = can + self.sampling_rate

        return y[:point]

class Track():
    def __init__(self, name, no, data):
        self.no = no
        self.score_data = data
        self.import_settings(name)

    # iniファイルから設定をインポートし、インスタンス変数に格納
    def import_settings(self, name):
        inifile = cp.SafeConfigParser()
        inifile.read("./data/settings/" + name + ".ini")
        try:
            settings = inifile["track" + str(self.no)]
        except KeyError:
            try:
                settings = inifile["DEFAULT"]
            except KeyError as e:
                print(e)
                exit(1)
        except Exception as e:
            print(e)
            exit(1)

        for key, val in settings.items():
            try:
                setattr(self, key, float(val))
            except ValueError:
                setattr(self, key, val)

    # トラックの生成
    def gen_track(self, sampling_rate, bpm):
        DEFAULT_LENGTH = 180
        WHOLE_NOTE = (60 / bpm) * 4  # 全音符の秒数
        y = np.zeros(sampling_rate * DEFAULT_LENGTH)

        for idx, elm in enumerate(self.score_data):
            if idx + 1 < len(self.score_data) and self.in_next(elm[0], self.score_data[idx + 1][0]):
                elm[1] -= self.interval / 1000
            tmp = self.gen_unit(elm, sampling_rate, WHOLE_NOTE)
            x = math.ceil(sampling_rate * (elm[2] * WHOLE_NOTE))
            y[x:x + len(tmp)] += tmp

        return y * self.volume

    # 次の音に現在の音と同じ音階が含まれているか判定
    def in_next(self, current, next):
        for item_c in current:
            for item_n in next:
                if item_c[0] == item_n[0]:
                    return True
        return False

    # 単音/和音の生成
    def gen_unit(self, notes, sampling_rate, whole_note):
        unit_length = whole_note * notes[1]  # ユニットの時間的な長さ
        y = []

        for note in notes[0]:
            freq = sw.note_to_freq(note[0])
            # 波のvelocityを調整
            tmp = sw.gen_wave(unit_length, freq, sampling_rate, self.waveform_type) * note[1]
            # エンベロープ処理を施してリストに追加
            y.append(sw.add_release(sw.add_attack(tmp, self.attack, sampling_rate), self.release, sampling_rate))

        return sw.synthesize_wave(y)
