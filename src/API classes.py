from abc import ABC, abstractmethod
import requests

class API_platform(ABC):
    """
    Абстрактный класс для работы с API разных платформ
    """

    @abstractmethod
    def get_vacancies(self, keyword: str):

        """
        Производит поиск вакансий на платформе по заданному ключевому слову и обрабатывает полученный список.
        :return: Список словарей с необходимыми параметрами вакансий
        """


class HeadHunter_API(API_platform):
    """
    Класс для работы с API платформы HeadHunter
    """

    def __init__(self, url='https://api.hh.ru/vacancies'):
        self.__url = url

    def get_vacancies(self, keyword: str):

        params = {'text': keyword, 'page': 0, 'per_page': 100}
        request = requests.get(self.__url, params=params)

        data = request.json()['items']

        vacancies = []

        for item in data:
            vacancy = {
                'name': item['name'], 'url': item['alternate_url'], 'employment': item['employment']['name'],
                'experience': item['experience']['name'], 'area': item['area']['name']
            }
            if item['salary'] is None:
                vacancy['salary'] = 'По договоренности'
            else:
                if item['salary']['from'] is None:
                    vacancy['min_salary'] = 'Минимальная зарплата не указана'
                else:
                    vacancy['min_salary'] = item['salary']['from']

                if item['salary']['to'] is None:
                    vacancy['max_salary'] = 'Максимальная зарплата не указана'
                else:
                    vacancy['max_salary'] = item['salary']['to']
                vacancy['currency'] = item['salary']['currency']

            vacancies.append(vacancy)

        return vacancies


class SuperJob_API(API_platform):
    """
    Класс для работы с API платформы SuperJob
    """

    pass
