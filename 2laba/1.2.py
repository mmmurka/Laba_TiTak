import math

def build_hamming_code(text):
    binary_text = convert_text_to_binary(text)
    control_bits_count = calculate_control_bits_count(len(binary_text))
    hamming_code = add_control_bits(binary_text, control_bits_count)
    return hamming_code

def convert_text_to_binary(text):
    binary_builder = []
    for c in text:
        binary_char = format(ord(c), '08b')
        binary_builder.append(binary_char)
    return ''.join(binary_builder)

def calculate_control_bits_count(data_bits_count):
    r = 0
    while 2 ** r < data_bits_count + r + 1:
        r += 1
    return r

def add_control_bits(data, control_bits_count):
    n = len(data)
    total_bits = n + control_bits_count
    hamming_code = ['0'] * total_bits

    data_index = 0
    for i in range(total_bits):
        if (i & (i + 1)) == 0:
            hamming_code[i] = '0'
        else:
            hamming_code[i] = data[data_index]
            data_index += 1

    for i in range(control_bits_count):
        parity_bit_index = 2 ** i - 1
        parity = calculate_parity(hamming_code, parity_bit_index)
        hamming_code[parity_bit_index] = '0' if parity == 0 else '1'

    return ''.join(hamming_code)

def calculate_parity(data, position):
    parity = 0
    length = len(data)
    for i in range(position, length, (position + 1) * 2):
        for j in range(i, min(i + position + 1, length)):
            if data[j] == '1':
                parity ^= 1
    return parity

def introduce_error(hamming_code, bit_index):
    if bit_index >= len(hamming_code) or bit_index < 0:
        raise ValueError("Недійсний індекс біта")

    hamming_array = list(hamming_code)
    hamming_array[bit_index] = '1' if hamming_array[bit_index] == '0' else '0'

    return ''.join(hamming_array)

def check_errors(hamming_code):
    control_bits_count = int(math.ceil(math.log2(len(hamming_code) + 1)))
    error_bit_index = 0

    for i in range(control_bits_count):
        parity_bit_index = 2 ** i - 1
        calculated_parity = calculate_parity(hamming_code, parity_bit_index)

        if calculated_parity != 0:
            error_bit_index += parity_bit_index + 1

    return error_bit_index


def main():
    text = """Кохайтеся, чорнобриві,
Та не з москалями,
Бо москалі — чужі люде,
Роблять лихо з вами.
Москаль любить жартуючи,
Жартуючи кине;
Піде в свою Московщину,
А дівчина гине..."""

    print("Вихідний текст:")
    print(text)

    def print_binary_with_line_break(binary_string):
        for i in range(0, len(binary_string), 70):
            print(binary_string[i:i + 70])

    hamming_code = build_hamming_code(text)
    print("\nХеммінг-код:")
    print_binary_with_line_break(hamming_code)



    # Припустимо, що ми введемо помилку випадкового біта
    error_index = 10
    tampered_hamming_code = introduce_error(hamming_code, error_index)
    print("\nХеммінг-код із введеною помилкою:")
    print(tampered_hamming_code)

    # Перевіряємо наявність помилок
    error_bit_index = check_errors(tampered_hamming_code)
    if error_bit_index != 0:
        print("\nВиявлено помилку в біті номер", error_bit_index)
    else:
        print("\nПомилка не виявлена.")


if __name__ == "__main__":
    main()
