from collections import Counter
import math

# Задана фраза
phrase = ("Кохайтеся, чорнобриві,"
          "Та не з москалями,"
          "Бо москалі — чужі люде,"
          "Роблять лихо з вами."
          "Москаль любить жартуючи,"
          "Жартуючи кине;"
          "Піде в свою Московщину,"
          "А дівчина гине...")

# Побудова гістограми частот символів
freq_histogram = Counter(phrase)

# Розрахунок загальної кількості символів у фразі
total_symbols = len(phrase)


# Виведення гістограми
print("Гістограма частот символів:")
for symbol, frequency in freq_histogram.items():
    print(f"Символ '{symbol}': {frequency} разів")

# Розрахунок загальної кількості символів у фразі
total_symbols = len(phrase)
print(f"\nЗагальна кількість символів у фразі: {total_symbols}")


# Функція для отримання бітового коду за ASCII
def ascii_code(text):
    binary_string = ""
    for char in text:
        binary_string += format(ord(char), '08b')  # конвертуємо символ в ASCII та додаємо його бітовий код
    return binary_string


# Функція для отримання бітового коду за кодом Грея
def gray_code(text):
    binary_string = ""
    prev_bit = '0'
    for char in text:
        ascii_val = ord(char)
        gray_val = ascii_val ^ (ascii_val >> 1)  # обчислюємо код Грея
        binary_string += format(gray_val, '08b')  # додаємо бітовий код Грея
    return binary_string


# Функція для розрахунку середньої довжини кодового слова
def calculate_average_code_length(frequencies, binary_string):
    # Загальна довжина бітового рядка - сума добутків частоти символу на довжину його бітового коду
    total_length = sum(frequencies[symbol] * len(binary_string) for symbol in frequencies)
    # Середнє значення довжини кодових слів - загальна довжина розділена на загальну кількість символів
    return total_length / sum(frequencies.values())


# Функція для розрахунку ентропії
def calculate_entropy(frequencies, total_symbols):
    entropy = 0
    for symbol, frequency in frequencies.items():
        # Обчислення ймовірності входження символу
        probability = frequency / total_symbols
        # Додавання внеску символу в ентропію
        entropy -= probability * math.log2(probability)
    return entropy


# Функція для розрахунку коефіцієнта ефективності
def calculate_efficiency(entropy, average_code_length):
    # Коефіцієнт ефективності - відношення ентропії до середньої довжини кодових слів
    return entropy / average_code_length


# Функція для розрахунку коефіцієнта стиснення
def calculate_compression_ratio(original_length, compressed_length):
    # Коефіцієнт стиснення - відношення довжини оригінальних даних до довжини стислого бітового рядка
    return original_length / compressed_length


# Розрахунок середньої довжини кодового слова для ASCII коду
average_code_length_ascii = calculate_average_code_length(freq_histogram, ascii_code(phrase))
print("Середня довжина кодового слова (ASCII):", average_code_length_ascii)

# Розрахунок середньої довжини кодового слова для коду Грея
average_code_length_gray = calculate_average_code_length(freq_histogram, gray_code(phrase))
print("Середня довжина кодового слова (код Грея):", average_code_length_gray)

# Розрахунок ентропії
entropy = calculate_entropy(freq_histogram, total_symbols)
print("Ентропія:", entropy)

# Перевірка оптимальності за Крафтом
ascii_kraft_passed = average_code_length_ascii >= entropy
gray_kraft_passed = average_code_length_gray >= entropy

# Перевірка оптимальності за Шенноном
ascii_shannon_passed = average_code_length_ascii >= entropy
gray_shannon_passed = average_code_length_gray >= entropy

# Виведення результатів перевірок за Крафтом
if ascii_kraft_passed and gray_kraft_passed:
    print("Перевірка оптимальності за Крафтом: Пройдено")
else:
    print("Перевірка оптимальності за Крафтом: Не пройдено")

# Виведення результатів перевірок за Шенноном
if ascii_shannon_passed and gray_shannon_passed:
    print("Перевірка оптимальності за Шенноном: Пройдено")
else:
    print("Перевірка оптимальності за Шенноном: Не пройдено")

# Розрахунок коефіцієнта ефективності для ASCII коду
efficiency_ascii = calculate_efficiency(entropy, average_code_length_ascii)
print("Коефіцієнт ефективності (ASCII):", efficiency_ascii)

# Розрахунок коефіцієнта ефективності для коду Грея
efficiency_gray = calculate_efficiency(entropy, average_code_length_gray)
print("Коефіцієнт ефективності (код Грея):", efficiency_gray)

# Розрахунок коефіцієнта стиснення для ASCII коду
compression_ratio_ascii = calculate_compression_ratio(total_symbols * 8, len(ascii_code(phrase)))
print("Коефіцієнт стиснення (ASCII):", compression_ratio_ascii)

# Розрахунок коефіцієнта стиснення для коду Грея
compression_ratio_gray = calculate_compression_ratio(total_symbols * 8, len(gray_code(phrase)))
print("Коефіцієнт стиснення (код Грея):", compression_ratio_gray)


def print_binary_with_line_break(binary_string):
    for i in range(0, len(binary_string), 70):
        print(binary_string[i:i+70])


# Виклик функцій та виведення результатів
ascii_binary = ascii_code(phrase)
gray_binary = gray_code(phrase)

len_ascii = len(ascii_binary)
len_gray = len(gray_binary)

print("\n\nБітовий код за ASCII:\n")
print_binary_with_line_break(ascii_binary)
print(f"\nЗагальна кількість символів ASCII: {len_ascii}")

print("\n\nБітовий код за кодом Грея:\n")
print_binary_with_line_break(gray_binary)
print(f"\nЗагальна кількість символів кодом Грея: {len_gray}")
