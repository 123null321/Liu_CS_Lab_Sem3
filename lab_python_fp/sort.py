# sort.py

data = [4, -30, 100, -100, 123, 1, 0, -1, -4]

if __name__ == '__main__':
    # 方式 1：不使用 lambda
    result = sorted(data, key=abs, reverse=True)
    print(result)

    # 方式 2：使用 lambda
    result_with_lambda = sorted(data, key=lambda x: abs(x), reverse=True)
    print(result_with_lambda)
