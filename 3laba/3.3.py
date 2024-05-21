import numpy as np
import matplotlib.pyplot as plt

# Допустим, это значения, полученные после квантования
quantized_values = np.array([1, 0.5, 1, 0.5, 1])  # Примерные значения

# Преобразование значений в двоичный код
# Предположим, что количество бит на уровень квантования - 3 (для 8 уровней)
bits_per_level = 3
binary_values = [np.binary_repr(int(val * (2**bits_per_level - 1)), width=bits_per_level) for val in quantized_values]

# Восстановление сигнала
reconstructed_values = [int(b, 2) / (2**bits_per_level - 1) for b in binary_values]

# Визуализация
plt.figure(figsize=(10, 5))
plt.plot(reconstructed_values, label='Reconstructed Signal', marker='o')
plt.title('Reconstructed Signal from Quantized Values')
plt.xlabel('Sample Number')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.show()

# Вывод бинарных значений для проверки
print("Binary values of quantized signal:", binary_values)