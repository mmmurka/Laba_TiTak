import numpy as np
import matplotlib.pyplot as plt

# Вхідні параметри
amplitude = 1.0  # Амплітуда
carrier_frequency = 0.82  # Частота несучої хвилі
modulation_frequency = 46.77  # Частота модуляції
sampling_rate = 1000  # Частота дискретизації
duration = 1.0  # Тривалість сигналу

# Часовий вектор
t = np.linspace(0, duration, int(sampling_rate * duration))

# Сигнал несучої хвилі
carrier_signal = amplitude * np.sin(2 * np.pi * carrier_frequency * t)

# Сигнал модуляції
modulation_signal = np.cos(2 * np.pi * modulation_frequency * t)

# Модульований сигнал
modulated_signal = carrier_signal * modulation_signal

# Побудова графіка
plt.figure(figsize=(10, 6))
plt.plot(t, modulated_signal, label='Модульований сигнал')
plt.plot(t, carrier_signal, label='Несучий сигнал')
plt.xlabel('Час')
plt.ylabel('Амплітуда')
plt.title('Модульований і несучий сигнали')
plt.legend()
plt.grid(True)
plt.show()
