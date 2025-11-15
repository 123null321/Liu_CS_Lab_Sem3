# field.py

def field(items, *args):
    """
    Генератор field:
    - items: список словарей
    - *args: список полей
    """
    assert len(args) > 0, "Нужно указать хотя бы одно имя поля"

    # 只有一个字段名：依次返回该字段的值（过滤掉 None）
    if len(args) == 1:
        key = args[0]
        for item in items:
            if key in item and item[key] is not None:
                yield item[key]
    # 多个字段名：为每个元素构造一个只包含这些字段的新 dict
    else:
        for item in items:
            new_dict = {}
            for key in args:
                if key in item and item[key] is not None:
                    new_dict[key] = item[key]
            if new_dict:     # 全是 None 的元素要被跳过
                yield new_dict


if __name__ == '__main__':
    goods = [
        {'title': 'Ковер', 'price': 2000, 'color': 'green'},
        {'title': 'Диван для отдыха', 'color': 'black'}
    ]

    print(list(field(goods, 'title')))
    print(list(field(goods, 'title', 'price')))
