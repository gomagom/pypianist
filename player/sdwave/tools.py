import numpy as np

# 音階→周波数
def note_to_freq(notestr):
    keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    key, octave = notestr[:-1], notestr[-1]

    try:
        octave = int(octave)
    except ValueError:
        print("オクターブに整数値以外が指定されました。")
        return False
    if 0 > octave or (1 > octave and not "A" <= key[0] <= "B"):
        print("存在しない音域が指定されました。最下音はA0(27.5Hz)です")
        return False

    if key not in keys:
        print("不正な音階が指定されました")
        return False

    # 周波数起点はA（ラ）からなのに、オクターブはC（ド）からなので周期を調整する
    return 27.5 * 2 ** (int(octave) + (keys.index(key) - 9) / 12)

# 音波の合成
def synthesize_wave(waves):
    return np.sum(waves, axis = 0)

# アタックを付与
def add_attack(wave, time_ms, sampling_rate):
    f = np.linspace(0, 1, round(sampling_rate * time_ms / 1000) + 1)
    return wave * np.concatenate([f, np.ones(len(wave) - len(f))])

# リリースを付与
def add_release(wave, time_ms, sampling_rate):
    f = np.linspace(1, 0, round(sampling_rate * time_ms / 1000) + 1)
    return wave * np.concatenate([np.ones(len(wave) - len(f)), f])