from collections import Counter


def shannon_fano_coding(text):
    # Рахуємо частоту кожного символу у тексті
    freq = Counter(text)
    # Сортуємо символи за спаданням їх частоти
    sorted_freq = {k: v for k, v in sorted(freq.items(), key=lambda item: item[1], reverse=True)}

    # Рекурсивна функція для побудови коду Шеннона-Фано
    def build_code(symbols, code=''):
        # Якщо в словнику лише один символ, повертаємо його код
        if len(symbols) == 1:
            return {list(symbols.keys())[0]: code}
        split = 0
        total_freq = sum(symbols.values())
        current_freq = 0
        # Знаходимо розділений індекс у списку символів
        for i, (symbol, freq) in enumerate(symbols.items()):
            current_freq += freq
            # Якщо поточна частота перевищує половину загальної частоти, зупиняємося
            if current_freq >= total_freq / 2:
                split = i
                break
        # Розділяємо символи на дві множини
        left_symbols = dict(list(symbols.items())[:split + 1])
        right_symbols = dict(list(symbols.items())[split + 1:])
        # Побудова коду для лівої та правої множини, додаючи відповідні біти
        code_dict = {}
        code_dict.update(build_code(left_symbols, code + '0'))
        code_dict.update(build_code(right_symbols, code + '1'))
        return code_dict

    # Побудова коду Шеннона-Фано
    code_dict = build_code(sorted_freq)

    return code_dict


def calculate_statistics(text, code_dict):
    total_bits = 0
    # Обчислення загальної кількості біт у закодованому тексті
    for char in text:
        total_bits += len(code_dict[char])
    average_length = total_bits / len(text)
    # Обчислення ентропії тексту
    entropy = sum([-freq / len(text) * (freq / len(text)) for freq in Counter(text).values()])
    # Обчислення коефіцієнта ефективності та коефіцієнта стиснення
    efficiency = entropy / average_length
    compression_ratio = 8 / average_length
    return total_bits, average_length, efficiency, compression_ratio


def check_kraft_inequality(code_dict):
    kraft_sum = sum([2**-len(code) for code in code_dict.values()])
    return abs(kraft_sum - 1) < 1e-9  # Перевіряємо, чи сума близька до 1 з точністю 1e-9


def check_shannon_optimality(text, code_dict):
    entropy = sum([-freq / len(text) * (freq / len(text)) for freq in Counter(text).values()])
    average_length = sum([len(code) * freq / len(text) for char, freq in Counter(text).items()
                          for code_char, code in code_dict.items() if char == code_char])
    return abs(entropy - average_length) < 1e-9  # Перевіряємо, чи середня довжина близька до ентропії з точністю 1e-9


def decode_text(encoded_text, code_dict):
    decoded_text = ""
    current_code = ""
    for bit in encoded_text:
        current_code += bit
        for char, code in code_dict.items():
            if code == current_code:
                decoded_text += char
                current_code = ""
                break
    return decoded_text


def main():
    # Вхідний текст
    text = ("Кохайтеся, чорнобриві, "
            "Та не з москалями, "
            "Бо москалі — чужі люде, "
            "Роблять лихо з вами. "
            "Москаль любить жартуючи, "
            "Жартуючи кине; "
            "Піде в свою Московщину, "
            "А дівчина гине... ")

    # Побудова словника кодів Шеннона-Фано
    code_dict = shannon_fano_coding(text)
    print("Словник кодів Шеннона-Фано:")
    for symbol, code in code_dict.items():
        print(f"Символ '{symbol}': {code}")

    # Результати статистичного аналізу
    total_bits, average_length, efficiency, compression_ratio = calculate_statistics(text, code_dict)
    print("\nРезультати статистичного аналізу:")
    print("Загальна довжина бітового рядка:", total_bits, "біт")
    print("Середня довжина кодових слів:", average_length, "біт на символ")
    print("Коефіцієнт ефективності:", efficiency)
    print("Коефіцієнт стиснення:", compression_ratio)

    # Перевірка оптимальності за Крафтом
    kraft_optimal = check_kraft_inequality(code_dict)
    if kraft_optimal:
        print("Код Шеннона-Фано є оптимальним за Крафтом")
    else:
        print("Код Шеннона-Фано не є оптимальним за Крафтом")

    # Перевірка оптимальності за Шенноном
    shannon_optimal = check_shannon_optimality(text, code_dict)
    if shannon_optimal:
        print("Код Шеннона-Фано є оптимальним за Шенноном")
    else:
        print("Код Шеннона-Фано не є оптимальним за Шенноном")

        # Побудова словника кодів Шеннона-Фано
        code_dict = shannon_fano_coding(text)

        # Закодований текст
        encoded_text = "".join([code_dict[char] for char in text])

        # Декодуємо текст та виводимо результат
        decoded_text = decode_text(encoded_text, code_dict)
        print("Декодований текст:")
        print(decoded_text)


if __name__ == "__main__":
    main()
