from tkinter import font
import numpy as np
import matplotlib.pyplot as plt

def _zero(_, t):
    return t * 0

# 正弦波
def _sine(freq, t):
    return np.sin(2 * np.pi * freq * t)

# 矩形波（50%パルス波）
def _square(freq, t):
    # [0-pi] -> 1, [pi-2pi] -> -1
    return (np.ceil(t * freq * 2) % 2) * 2 - 1

# 25%パルス波
def _pulse_quarter(freq, t):
    return (np.ceil(t * freq * 4 - 1) % 4 == 0) * 2 - 1

# 12.5%パルス波
def _pulse_eighth(freq, t):
    return (np.ceil(t * freq * 8 - 1) % 8 == 0) * 2 - 1

# 三角波
def _triangle(freq, t):
    return np.abs((2 * t * freq - 1 / 2) % 2 - 1) * 2 - 1

# 階段三角波
def _triangle_stair(freq, t):
    s = np.abs((2 * t * freq - 1 / 2) % 2 - 1) * 16 + 0.5
    return s.astype("int64") / 8 - 1

# 階段三角波（ファミコン）
def _triangle_stair2(freq, t):
    s = list(range(16)) + list(range(15, -1, -1))
    t = (t * len(s) * freq) % len(s)
    return np.array([s[int(i)] / 7.5 - 1 for i in t])

# のこぎり波
def _sawtooth(freq, t):
    p = t.copy()
    return ((2 * p * freq) % 2) - 1

# ノイズ(ファミコン風)
def _noise(freq, t):
    duration = t[-1]-t[0]
    coarse_x = np.linspace(t[0], t[-1], int(freq*20*duration)+1) # ここの倍率は要検討
    coarse_noise = np.random.uniform(-1, 1, size=coarse_x.shape[0])
    # 一次元のNearest Neighbor法
    tile_n = int(np.ceil(t.shape[0]/coarse_x.shape[0]))
    interpolate_noise = np.stack([coarse_noise for i in range(tile_n)], axis=-1)
    return interpolate_noise.flatten()[:t.shape[0]]

sampling_rate = 100
x = np.linspace(0, 2, sampling_rate * 2 + 1)
freq = 10
y = _square(freq, x)

# plt.figure(figsize=(10, 2))
# plt.plot(x, y)
# plt.grid()
# plt.savefig("./tests/triangle_stair.png")

y_f = np.fft.fft(y) # 波形のフーリエ変換
freqs = np.fft.fftfreq(len(y)) * sampling_rate # サンプリング周波数を返す

# # グラフ表示
# plt.figure()
# plt.rcParams['font.family'] = 'Times New Roman'
# plt.rcParams['font.size'] = 17
# plt.subplot(121)
# plt.plot(x, y, label='f(n)')
# plt.xlabel("Time", fontsize=20)
# plt.ylabel("Signal", fontsize=20)
# plt.grid()
# leg = plt.legend(loc=1, fontsize=25)
# leg.get_frame().set_alpha(1)
# plt.subplot(122)
# plt.plot(freqs, Amp, label='|F(k)|')
# plt.xlabel('Frequency', fontsize=20)
# plt.ylabel('Amplitude', fontsize=20)
# plt.grid()
# leg = plt.legend(loc=1, fontsize=25)
# leg.get_frame().set_alpha(1)
# plt.show()

# plt.figure(figsize=(2, 2))
fig2, ax2= plt.subplots()
ax2.stem(freqs, np.abs(y_f), use_line_collection=True) # フーリエ変換の結果をステム(茎)プロットする
ax2.set_xlabel('周波数[Hz]', fontname="MS Gothic", fontsize=15)
ax2.set_ylabel('スペクトラム密度', fontname="MS Gothic", fontsize=15)
ax2.set_xlim(- sampling_rate / 2, sampling_rate / 2)
ax2.set_ylim(-5, sampling_rate * 1.3)

plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.savefig("./tests/spec.png")
plt.show()