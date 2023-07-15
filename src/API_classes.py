from abc import ABC, abstractmethod
import requests
import os


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
                'area': item['area']['name']
            }

            if item['experience']['name'] == 'Нет опыта':
                vacancy['experience'] = 'Без опыта'
            elif item['experience']['name'] == 'От 1 года до 3 лет':
                vacancy['experience'] = 'От 1 года'
            elif item['experience']['name'] == 'От 3 до 6 лет':
                vacancy['experience'] = 'От 3 лет'
            elif item['experience']['name'] == 'Более 6 лет':
                vacancy['experience'] = 'От 6 лет'
            else:
                vacancy['experience'] = 'Не имеет значения'

            if item['salary'] is None:
                vacancy['min_salary'] = 'По договоренности'
                vacancy['max_salary'] = 'По договоренности'
                vacancy['currency'] = 'Не указано'
            else:
                if item['salary']['from'] is None:
                    vacancy['min_salary'] = 'Минимальная зарплата не указана'
                else:
                    vacancy['min_salary'] = item['salary']['from']

                if item['salary']['to'] is None:
                    vacancy['max_salary'] = 'Максимальная зарплата не указана'
                else:
                    vacancy['max_salary'] = item['salary']['to']
                if item['salary']['currency'] == 'RUR':
                    vacancy['currency'] = 'RUB'
                else:
                    vacancy['currency'] = item['salary']['currency']

            vacancies.append(vacancy)

        return vacancies


class SuperJob_API(API_platform):
    """
    Класс для работы с API платформы SuperJob
    """

    def __init__(self, url='https://api.superjob.ru/2.0/vacancies/'):
        self.__url = url

    def get_vacancies(self, keyword: str):

        sj_api_key: str = os.getenv('SJ_API_KEY')

        headers = {'X-Api-App-Id': sj_api_key}
        params = {'keyword': keyword, 'count': 100}

        request = requests.get(self.__url, headers=headers, params=params)

        data = request.json()['objects']

        vacancies = []

        for item in data:
            vacancy = {
                'name': item['profession'], 'url': item['link'], 'employment': item['type_of_work']['title'],
                'area': item['town']['title'], 'experience': item['experience']['title']
            }
            if item['payment_from'] == item['payment_to'] == 0:
                vacancy['min_salary'] = 'По договоренности'
                vacancy['max_salary'] = 'По договоренности'
                vacancy['currency'] = 'Не указано'
            else:
                if item['payment_from'] == 0:
                    vacancy['min_salary'] = 'Минимальная зарплата не указана'
                    vacancy['currency'] = 'Не указано'
                else:
                    vacancy['min_salary'] = item['payment_from']
                    vacancy['currency'] = item['currency']

                if item['payment_to'] == 0:
                    vacancy['max_salary'] = 'Максимальная зарплата не указана'
                else:
                    vacancy['max_salary'] = item['payment_to']
                    vacancy['currency'] = item['currency']

            vacancies.append(vacancy)

        return vacancies
