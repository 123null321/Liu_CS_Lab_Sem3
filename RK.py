from operator import itemgetter

class Operator:
    """Оператор языка программирования"""
    def __init__(self, id, name, complexity, lang_id):
        self.id = id                  
        self.name = name              
        self.complexity = complexity  
        self.lang_id = lang_id        


class Language:
    """Язык программирования"""
    def __init__(self, id, name):
        self.id = id          
        self.name = name      


class OperLang:
    """
    'Операторы языка' для реализации связи многие-ко-многим
    """
    def __init__(self, lang_id, op_id):
        self.lang_id = lang_id  
        self.op_id = op_id      



langs = [
    Language(1, 'Ада'),
    Language(2, 'Питон'),
    Language(3, 'Алгол'),
    Language(4, 'С++'),
]

operators = [
    Operator(1, 'Иванов', 3, 1),   
    Operator(2, 'Петров', 5, 2),   
    Operator(3, 'Сидоров', 2, 2),  
    Operator(4, 'Смирнов', 4, 3),  
    Operator(5, 'Кнут', 1, 4),     
]


opers_langs = [
    OperLang(1, 1),  
    OperLang(2, 2),  
    OperLang(2, 3),  
    OperLang(3, 4),  
    OperLang(4, 5),  
    OperLang(1, 2),  
    OperLang(3, 1),  
]


def main():
    """Основная функция"""

   
    one_to_many = [
        (op.name, op.complexity, lang.name)
        for lang in langs
        for op in operators
        if op.lang_id == lang.id
    ]

    many_to_many_temp = [
        (lang.name, ol.lang_id, ol.op_id)
        for lang in langs
        for ol in opers_langs
        if lang.id == ol.lang_id
    ]

    many_to_many = [
        (op.name, op.complexity, lang_name)
        for lang_name, lang_id, op_id in many_to_many_temp
        for op in operators if op.id == op_id
    ]

    # ───────── Задание Д1 ─────────
    print('Задание Д1')
    res_d1 = sorted(
        [(name, lang_name) for name, _, lang_name in one_to_many
         if name.endswith('ов')],
        key=itemgetter(0)  
    )
    print(res_d1)

    # ───────── Задание Д2 ─────────
    print('\nЗадание Д2')
    
    res_d2_unsorted = []

    for lang in langs:
        lang_ops = list(filter(lambda i: i[2] == lang.name, one_to_many))
        if len(lang_ops) > 0:
            complexities = [complexity for _, complexity, _ in lang_ops]
            avg_complexity = sum(complexities) / len(complexities)
            res_d2_unsorted.append((lang.name, avg_complexity))

    
    res_d2 = sorted(res_d2_unsorted, key=itemgetter(1))
    print(res_d2)

    # ───────── Задание Д3 ─────────
    print('\nЗадание Д3')
    
    res_d3 = {}
    for lang in langs:
        if lang.name.startswith('А'):
            
            lang_ops = list(filter(lambda i: i[2] == lang.name, many_to_many))
            op_names = [name for name, _, _ in lang_ops]
            res_d3[lang.name] = op_names

    print(res_d3)


if __name__ == '__main__':
    main()
