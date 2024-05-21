import numpy as np
import matplotlib.pyplot as plt

# Параметры времени
T = 20  # Общее время сигнала
f = 0.82  # Частота модуляции
fs = 46.77  # Частота дискретизации (количество отсчетов в секунду)
t = np.linspace(0, T, int(T * fs))  # Вектор времени

# Определение функции s(t)
# Для примера предполагаем, что каждый уровень длится приблизительно равное время
s = np.zeros_like(t)
s[:int(len(t)/3)] = 1  # Первый уровень
s[int(len(t)/3):int(2*len(t)/3)] = 0.5  # Второй уровень
s[int(2*len(t)/3):] = 1  # Третий уровень

# Модулирующий сигнал
w = s * np.sin(2 * np.pi * f * t)

# Визуализация
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.title("Original Signal s(t)")
plt.plot(t, s, label='s(t)')
plt.ylabel("Amplitude")
plt.legend()

plt.subplot(2, 1, 2)
plt.title("Modulated Signal w(t)")
plt.plot(t, w, label='w(t) = s(t) * sin(2πft)', color='red')
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.legend()
plt.tight_layout()
plt.show()