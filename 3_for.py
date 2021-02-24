"""

Домашнее задание №1

Цикл for: Оценки

* Создать список из словарей с оценками учеников разных классов 
  школы вида [{'school_class': '4a', 'scores': [3,4,4,5,2]}, ...]
* Посчитать и вывести средний балл по всей школе.
* Посчитать и вывести средний балл по каждому классу.
"""
import random


def rating_generator(name: str, quantity: int) -> dict:
    """
    Случайное генерирование оценок для класса name состоящего из quantity человек
    """
    return {'school_class': name, 'scores': [random.randint(2, 5) for i in range(quantity)]}


def average_score(rating: list) -> float:
    return sum(rating) / len(rating)


def main():
    """
    Эта функция вызывается автоматически при запуске скрипта в консоли
    В ней надо заменить pass на ваш код
    """
    # Название классов школы и число учеников
    school_classes = [
        ('4a', 15), ('4б', 12), ('4в', 22), ('5а', 17), ('5б', 27), ('5в', 16),
    ]

    rating_list = [
        {'school_class': 'super_class', 'scores': [5, 5, 5, 5, 5, 5, 5, 5]},
        {'school_class': 'good_class', 'scores': [4, 4, 4, 4, 4, 4, 4, 4]},
        {'school_class': 'bad_class', 'scores': [2, 2, 2, 2, 2, 2, 2, 2]},
    ]

    # заполняем список из словарей с оценками учеников разных классов школы
    for school_class in school_classes:
        rating_list.append(rating_generator(*school_class))
    print("Cписок из словарей с оценками учеников разных классов школы:\n", rating_list)

    # считаем средние баллы по всей школе и каждому классу
    school_score_rating = {}
    for rating in rating_list:
        school_score_rating[rating['school_class']] = average_score(rating['scores'])
    print("Средний балл по всей школе = ", average_score(school_score_rating.values()))
    print('Средний балл по каждому классу:')
    for name, score in school_score_rating.items():
        print(f"{name} = {score}")


if __name__ == "__main__":
    main()
