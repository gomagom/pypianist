import numpy as np
import matplotlib.pyplot as plt

# 階段三角波
def _triangle_stair(freq, t):
    s = np.abs((2 * t * freq - 1 / 2) % 2 - 1) * 16 + 0.5
    return s.astype("int64") / 8 - 1

# 階段三角波（ファミコン）
def _triangle_stair2(freq, t):
    s = list(range(16)) + list(range(15, -1, -1))
    t = (t * len(s) * freq + 8) % len(s)
    return np.array([s[int(i)] / 7.5 - 1 for i in t])

x = np.linspace(0, 2, 44100 * 2 + 1)
y = _triangle_stair2(2, x)
plt.plot(x, y)
plt.show()
