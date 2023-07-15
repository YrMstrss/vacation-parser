from API_classes import HeadHunter_API, SuperJob_API
from vacancy import Vacancy


def get_filters() -> tuple:
    print('Для пропуска нежелательных фильтров нажмите Enter')

    town = input('В каком городе ищем вакансии?\n')

    currency = input('Введите желаемую валюту (RUB, USD, EUR): \n')

    if currency is not None:
        payment = input('Введите минимальную желаемую заработную плату: \n')

    experience = input('Ваш опыт работы (0 - без опыта, 1 - от 1 до 3 лет, 2 - от 3 до 6 лет, 3 - более 6 лет): \n')

    employment = input('Выберите желаемый тип занятости (1 - полный день, 2 - неполный день, 3 - сменный график, \n'
                       '4 - частичная занятость, 5 - временная работа, 6 - вахтовый метод, 7 - стажировка): ')

    return town, currency, payment, experience, employment


def search_without_filters(keyword, platform):
    hh = HeadHunter_API()
    hh_data = hh.get_vacancies(keyword)

    sj = SuperJob_API()
    sj_data = sj.get_vacancies(keyword)

    if platform == 1:
        data = hh_data

    elif platform == 2:
        data = sj_data

    elif platform == 3:
        data = hh_data + sj_data

    vacancies = []

    for item in data:
        vacancy = Vacancy(item)
        vacancies.append(vacancy)


def interaction_with_user():

    """
    Функция взаимодействия с пользователем
    :return:
    """

    keyword = input('Введите ключевое слово для поиска вакансий:\n')
    platform = int(input('На какой платформе будем искать вакансии? (1 - HH, 2 - SuperJob, 3 - обе):\n'))
    filters = input('Желаете ли применить фильтры к результатам поиска? (да/нет)\n')

    if filters.lower() == 'да':

        town, currency, payment, experience, employment = get_filters()

        if town != '':
            keyword += f' {town.lower().title()}'

    else:

        search_without_filters(keyword, platform)

