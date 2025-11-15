# gen_random.py

import random


def gen_random(num_count, begin, end):
    """
    生成 num_count 个 [begin, end] 区间的随机整数
    """
    for _ in range(num_count):
        yield random.randint(begin, end)


if __name__ == '__main__':
    print(list(gen_random(5, 1, 3)))
