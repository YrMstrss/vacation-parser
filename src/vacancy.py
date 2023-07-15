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


def write_info_to_json(vacancy: Vacancy, file_name='results.json'):
    vacancy_dict = {
        'Название вакансии': vacancy.name,
        'Ссылка на объявление': vacancy.url,
        'Тип занятости': vacancy.employment,
        'Опыт работы': vacancy.experience,
        'Город': vacancy.area,
        'Заработная плата': {
            'От': vacancy.min_salary,
            'До': vacancy.min_salary,
            'Валюта': vacancy.currency
        }
    }

    with open(file_name, 'w') as json_file:
        json.dump(vacancy_dict, json_file, indent=2, ensure_ascii=False)
