# unique.py

class Unique(object):
    """
    迭代器：遍历 items，自动去重
    ignore_case=True 时，字符串按小写比较
    """

    def __init__(self, items, **kwargs):
        self._iterator = iter(items)
        self.ignore_case = bool(kwargs.get('ignore_case', False))
        self._seen = set()

    def __iter__(self):
        return self

    def __next__(self):
        for item in self._iterator:
            # 根据 ignore_case 计算 “比较用的 key”
            if self.ignore_case and isinstance(item, str):
                key = item.lower()
            else:
                key = item

            if key in self._seen:
                continue

            self._seen.add(key)
            return item

        # 如果底层迭代用尽
        raise StopIteration


if __name__ == '__main__':
    from gen_random import gen_random

    data = [1, 1, 1, 2, 2]
    print(list(Unique(data)))

    data = gen_random(10, 1, 3)
    print(list(Unique(data)))

    data = ['a', 'A', 'b', 'B', 'a', 'A', 'b', 'B']
    print(list(Unique(data)))
    print(list(Unique(data, ignore_case=True)))
