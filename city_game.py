from collections import defaultdict
import settings


class CityGame:
    """ Класс для игры в города"""
    def __init__(self):
        self.score = 0
        self.last_char = None
        self._city_list = defaultdict(set)

    def _create_city_list(self):
        """
        создаётся словарь с множествами городов взятых с
        https://github.com/Braklord/DeskChan-Cities/blob/master/cities.db
        ключи словаря - первые буквы слов
        """
        with open(settings.CITY_DB_NAME, 'r', encoding='utf-8') as file:
            for line in file:
                city = line.strip().lower()
                self._city_list[city[0]].add(city)

    def start_new_game(self):
        """ Начинаем игру или обновляем """
        self.score = 0
        self._create_city_list()

    def check_last_char(self, player_city: str) -> bool:
        """ Проверяет начинается ли player_city на последний подходящий символ предыдущего города"""
        if player_city[0].lower() == self.last_char or self.last_char is None:
            return True
        return False

    def check_city(self, player_city: str) -> bool:
        """ Проверяет наличие player_city и удаляет его возвращая True, в противном случае False"""
        try:
            self._city_list[player_city[0]].remove(player_city)
        except KeyError:
            return False
        self.score += 1
        return True

    def _get_valid_last_char(self, city_name):
        """ Проходит по city_name начиная с конца, выбирает символ так, чтобы в базе были слова начинающиеся на него"""
        for char in city_name[::-1]:
            if char in self._city_list:
                return char
        raise KeyError

    def get_city(self, player_city: str):
        """
        Возвращает название города начинающееся на последний символ player_city,
        если в базе нет городов на эту букву то возвращает название начинающееся на предыдущий символ.
        Вернёт None когда подходящих городов нет.
        """
        try:
            last_char = self._get_valid_last_char(player_city)
            new_city = self._city_list[last_char].pop()
            self.last_char = self._get_valid_last_char(new_city)
        except KeyError:
            return None
        return new_city.capitalize()
