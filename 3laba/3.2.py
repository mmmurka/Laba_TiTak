import numpy as np
import matplotlib.pyplot as plt

# Параметры сигнала
T = 20  # Общее время сигнала
f = 0.82  # Частота модуляции
fs = 46.77  # Частота дискретизации
t = np.linspace(0, T, int(T * fs))  # Вектор времени

# Функция s(t)
s = np.zeros_like(t)
s[:int(len(t)/3)] = 1
s[int(len(t)/3):int(2*len(t)/3)] = 0.5
s[int(2*len(t)/3):] = 1

# Модулирующий сигнал
w = s * np.sin(2 * np.pi * f * t)

# Дискретизация и квантование сигнала
num_levels = 8  # Количество уровней квантования
w_quantized = np.round((w - np.min(w)) / (np.max(w) - np.min(w)) * (num_levels - 1)) * (np.max(w) - np.min(w)) / (num_levels - 1) + np.min(w)

# Визуализация результатов
plt.figure(figsize=(12, 8))
plt.subplot(3, 1, 1)
plt.plot(t, s, label='Original Signal s(t)')
plt.title('Original Signal s(t)')
plt.ylabel('Amplitude')
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(t, w, label='Modulated Signal w(t)', color='red')
plt.title('Modulated Signal w(t)')
plt.ylabel('Amplitude')
plt.grid(True)

plt.subplot(3, 1, 3)
plt.stem(t, w_quantized, linefmt='b-', markerfmt='bo', basefmt='r-')
plt.title('Quantized Signal')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.grid(True)

plt.tight_layout()
plt.show()