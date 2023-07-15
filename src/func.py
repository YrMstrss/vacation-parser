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


def get_hh_vacancies(keyword):
    """
    Обращается к классу HeadHunter_API для получения данных по ключевому слову
    :param keyword: Ключевое слово
    :return: Полученные данные
    """
    hh = HeadHunter_API()
    hh_data = hh.get_vacancies(keyword)

    return hh_data


def get_sj_vacancies(keyword):
    """
    Обращается к классу SuperJob_API для получения данных по ключевому слову
    :param keyword: Ключевое слово
    :return: Полученные данные:
    """
    sj = SuperJob_API()
    sj_data = sj.get_vacancies(keyword)

    return sj_data


def search_without_filters(keyword, platform):
    """
    Поиск вакансий по ключевому слову на заданной платформе без фильтров
    :param keyword: Ключевое слово
    :param platform: Номер платформы
    :return: Список вакансий
    """

    if platform == 1:
        vacancies_data = get_hh_vacancies(keyword)

    elif platform == 2:
        vacancies_data = get_sj_vacancies(keyword)

    elif platform == 3:
        vacancies_data = get_hh_vacancies(keyword) + get_sj_vacancies(keyword)

    return vacancies_data


# def search_with_filters(keyword, platform):
#     """
#     Поиск вакансий по ключевому слову на заданной платформе с заданными фильтрами
#     :param keyword: Ключевое слово
#     :param platform: Номер платформы
#     :return: Список вакансий
#     """
#
#     vacancies_data = search_without_filters(keyword, platform)
#
#     return vacancies_data


def interaction_with_user():

    """
    Функция взаимодействия с пользователем
    :return: Список словарей с вакансиями (data), список экземпляров класса Vacancy (vacancies)
    """

    keyword = input('Введите ключевое слово для поиска вакансий:\n')

    while True:
        platform = input('На какой платформе будем искать вакансии? (1 - HH, 2 - SuperJob, 3 - обе):\n')
        if platform == '1' or platform == '2' or platform == '3':
            break
        else:
            print('Введите корректное значение (1/2/3)')

    while True:
        filters = input('Желаете ли применить фильтры к результатам поиска? (да/нет)\n')
        if filters.lower() == 'да' or filters.lower() == 'нет':
            break
        else:
            print('Введите да или нет')

    if filters.lower() == 'да':

        town, currency, payment, experience, employment = get_filters()

        if town != '':
            keyword += f' {town.lower().title()}'

        # data = search_with_filters(keyword, platform)

    elif filters.lower() == 'нет':

        data = search_without_filters(keyword, int(platform))

    vacancies = []

    for item in data:
        vacancy = Vacancy(item)
        vacancies.append(vacancy)

    return data, vacancies
