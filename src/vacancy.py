import json


class Vacancy:

    """
    Класс вакансии
    """

    def __init__(self, vacancy_dict: dict):
        self.name = vacancy_dict['name']
        self.url = vacancy_dict['url']
        self.employment = vacancy_dict['employment']
        self.experience = vacancy_dict['experience']
        self.area = vacancy_dict['area']
        self.min_salary = vacancy_dict['min_salary']
        self.max_salary = vacancy_dict['max_salary']
        self.currency = vacancy_dict['currency']

    def make_dict(self):
        """
        Записывает данные о вакансии в json-подобном формате
        :return: Словарь с данными о вакансии
        """

        vacancy_dict = {
            'Название вакансии': self.name,
            'Ссылка на объявление': self.url,
            'Тип занятости': self.employment,
            'Опыт работы': self.experience,
            'Город': self.area,
            'Заработная плата': {
                'От': self.min_salary,
                'До': self.min_salary,
                'Валюта': self.currency
            }
        }

        return json.dumps(vacancy_dict, indent=2, ensure_ascii=False)


def write_info_to_json(vacancy_list: list, file_name='search_results.json'):
    """
    Записывает данные о найденных вакансиях в файл
    :param vacancy_list: Список словарей с данными о вакансиях
    :param file_name: Имя файла, в который будут записаны данные
    :return: None
    """

    with open(file_name, 'w') as json_file:
        json.dump(vacancy_list, json_file, indent=2, ensure_ascii=False)
