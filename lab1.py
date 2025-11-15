import sys
import math

def input_coefficient(name):
    while True:
        value = input(f"Введите коэффициент {name}: ")
        try:
            return float(value)
        except ValueError:
            print("Ошибка: введите число!")

def get_coefficients():
    coeffs = []
    for i, name in enumerate(["A", "B", "C"], start=1):
        try:
            value = float(sys.argv[i])
        except (IndexError, ValueError):
            value = input_coefficient(name)
        coeffs.append(value)
    return coeffs

def solve_biquadratic(a, b, c):
    if a == 0:
        print("Это не биквадратное уравнение (A=0).")
        return []

    d = b ** 2 - 4 * a * c
    print(f"Дискриминант: {d}")

    if d < 0:
        print("Нет действительных корней.")
        return []

    y1 = (-b + math.sqrt(d)) / (2 * a)
    y2 = (-b - math.sqrt(d)) / (2 * a)
    roots = []

    for y in [y1, y2]:
        if y >= 0:
            roots.extend([math.sqrt(y), -math.sqrt(y)])

    if roots:
        print("Действительные корни уравнения:", roots)
    else:
        print("Нет действительных корней.")

    return roots

def main():
    a, b, c = get_coefficients()
    solve_biquadratic(a, b, c)

if __name__ == "__main__":
    main()
