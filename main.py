from operator import itemgetter

# -----------------------------------------------------------------------------
# 1. Классы данных (Библиотека - Язык программирования)
# -----------------------------------------------------------------------------

class Lang:
    """Язык программирования (Many-side)"""
    def __init__(self, id, name, popularity, lib_id):
        self.id = id
        self.name = name
        self.popularity = popularity
        self.lib_id = lib_id


class Lib:
    """Библиотека (One-side)"""
    def __init__(self, id, name):
        self.id = id
        self.name = name


class LangLib:
    """
    'Языки программирования в библиотеке' для реализации
    связи многие-ко-многим
    """
    def __init__(self, lib_id, lang_id):
        self.lib_id = lib_id
        self.lang_id = lang_id


# -----------------------------------------------------------------------------
# 2. Функции для работы с данными
# -----------------------------------------------------------------------------

def get_one_to_many(libs, langs):
    """
    Создает соединение один-ко-многим

    Args:
        libs: список библиотек
        langs: список языков

    Returns:
        список кортежей (lang.name, lang.popularity, lib.name)
    """
    return [(l.name, l.popularity, b.name)
            for b in libs
            for l in langs
            if l.lib_id == b.id]


def get_many_to_many(libs, langs, lang_libs):
    """
    Создает соединение многие-ко-многим

    Args:
        libs: список библиотек
        langs: список языков
        lang_libs: список связей многие-ко-многим

    Returns:
        список кортежей (lang.name, lang.popularity, lib.name)
    """
    many_to_many_temp = [(b.name, ll.lib_id, ll.lang_id)
                         for b in libs
                         for ll in lang_libs
                         if b.id == ll.lib_id]

    return [(l.name, l.popularity, lib_name)
            for lib_name, lib_id, lang_id in many_to_many_temp
            for l in langs if l.id == lang_id]


def filter_langs_ending_with(one_to_many, ending):
    """
    Д1: Фильтрует языки по окончанию названия

    Args:
        one_to_many: соединение один-ко-многим
        ending: строка окончания для фильтрации

    Returns:
        отсортированный список языков и их библиотек
    """
    filtered = list(filter(lambda x: x[0].endswith(ending), one_to_many))
    return sorted(filtered, key=itemgetter(0))


def get_libs_avg_popularity(libs, one_to_many):
    """
    Д2: Вычисляет среднюю популярность языков для каждой библиотеки

    Args:
        libs: список библиотек
        one_to_many: соединение один-ко-многим

    Returns:
        список кортежей (lib.name, avg_popularity), отсортированный по убыванию
    """
    result = []
    for b in libs:
        b_langs = list(filter(lambda x: x[2] == b.name, one_to_many))

        if len(b_langs) > 0:
            b_popularities = [pop for _, pop, _ in b_langs]
            avg_popularity = sum(b_popularities) / len(b_popularities)
            result.append((b.name, avg_popularity))

    return sorted(result, key=itemgetter(1), reverse=True)


def get_libs_starting_with_langs(libs, many_to_many, prefix):
    """
    Д3: Получает библиотеки, начинающиеся с определенного префикса,
    и список языков в них

    Args:
        libs: список библиотек
        many_to_many: соединение многие-ко-многим
        prefix: префикс для фильтрации названий библиотек

    Returns:
        словарь {lib.name: [lang.name, ...]}
    """
    result = {}
    for b in libs:
        if b.name.startswith(prefix):
            b_langs = list(filter(lambda x: x[2] == b.name, many_to_many))
            b_lang_names = [name for name, _, _ in b_langs]
            result[b.name] = b_lang_names

    return result


# -----------------------------------------------------------------------------
# 3. Функция для получения тестовых данных
# -----------------------------------------------------------------------------


def get_test_data():
    """
    Возвращает тестовые данные

    Returns:
        кортеж (libs, langs, lang_libs)
    """
    libs = [
        Lib(1, 'Стандартная библиотека Python'),
        Lib(2, 'Библиотека для работы с данными'),
        Lib(3, 'Библиотека для веб-разработки'),
        Lib(4, 'Библиотека для машинного обучения'),
        Lib(5, 'Библиотека для научных вычислений'),
    ]

    langs = [
        Lang(1, 'Python', 10, 1),
        Lang(2, 'Java', 8, 2),
        Lang(3, 'JavaScript', 9, 3),
        Lang(4, 'C++', 7, 1),
        Lang(5, 'C#', 6, 2),
        Lang(6, 'Ruby', 4, 3),
        Lang(7, 'Go', 5, 4),
        Lang(8, 'Rust', 5, 4),
        Lang(9, 'Haskell', 2, 5),
        Lang(10, 'Scala', 3, 5),
    ]

    lang_libs = [
        LangLib(1, 1), LangLib(2, 1), LangLib(3, 1), LangLib(4, 1), LangLib(5, 1),
        LangLib(2, 2), LangLib(3, 3), LangLib(1, 4), LangLib(4, 7), LangLib(4, 8),
        LangLib(5, 9), LangLib(5, 10),
    ]

    return libs, langs, lang_libs


# -----------------------------------------------------------------------------
# 4. Основная функция
# -----------------------------------------------------------------------------

def main():
    """Основная функция"""
    libs, langs, lang_libs = get_test_data()

    one_to_many = get_one_to_many(libs, langs)
    many_to_many = get_many_to_many(libs, langs, lang_libs)

    print('Задание Д1 (Один-ко-многим)')
    res_d1 = filter_langs_ending_with(one_to_many, 'on')
    for item in res_d1:
        print(f'Язык: {item[0]}, Популярность: {item[1]}, Библиотека: {item[2]}')

    print('\nЗадание Д2 (Один-ко-многим)')
    res_d2 = get_libs_avg_popularity(libs, one_to_many)
    for lib_name, avg_pop in res_d2:
        print(f'Библиотека: {lib_name}, Средняя популярность: {avg_pop:.2f}')

    print('\nЗадание Д3 (Многие-ко-многим)')
    res_d3 = get_libs_starting_with_langs(libs, many_to_many, 'Б')
    for lib_name, lang_names in res_d3.items():
        print(f'Библиотека: {lib_name}')
        for lang_name in lang_names:
            print(f'  - {lang_name}')

if __name__ == "__main__":
    main()
