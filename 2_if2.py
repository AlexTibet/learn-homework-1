"""

Домашнее задание №1

Условный оператор: Сравнение строк

* Написать функцию, которая принимает на вход две строки
* Проверить, является ли то, что передано функции, строками. 
  Если нет - вернуть 0
* Если строки одинаковые, вернуть 1
* Если строки разные и первая длиннее, вернуть 2
* Если строки разные и вторая строка 'learn', возвращает 3
* Вызвать функцию несколько раз, передавая ей разные праметры 
  и выводя на экран результаты

"""


def string_checker(one_str, two_str):
    if not isinstance(one_str, str) or not isinstance(two_str, str):
        return 0
    if one_str == two_str:
        return 1
    if len(one_str) > len(two_str):
        return 2
    if two_str == 'learn':
        return 3
    else:
        return "неучтённый вариант: строки разные, вторая длиннее, и при этом не 'learn'"


def main():
    """
    Эта функция вызывается автоматически при запуске скрипта в консоли
    В ней надо заменить pass на ваш код
    """
    print(string_checker(1, '2'))  # 0
    print(string_checker('фыв', 2))  # 0
    print(string_checker('abc', 'abc'))  # 1
    print(string_checker('abcdef', 'abc'))  # 2
    print(string_checker('abcdef', 'learn'))  # 2
    print(string_checker('abc', 'learn'))  # 3
    print(string_checker('abcd', 'nolearn'))  # неучтённый вариант: строки разные, вторая длиннее, и при этом не 'learn'


if __name__ == "__main__":
    main()
