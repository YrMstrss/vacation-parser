from API_classes import HeadHunter_API, SuperJob_API
from vacancy import Vacancy


def get_filters() -> tuple:
    print('Для пропуска нежелательных фильтров нажмите Enter')

    town = input('В каком городе ищем вакансии?\n')

    currency = input('Введите желаемую валюту (RUB, USD, EUR): \n')

    if currency is not None:
        payment = input('Введите минимальную желаемую заработную плату: \n')

    while True:
        experience = int(input('Ваш опыт работы (0 - без опыта, 1 - от 1 до 3 лет, 2 - от 3 до 6 лет,'
                               '3 - более 6 лет): \n'))
        if experience == 0 or experience == 1 or experience == 2 or experience == 3:
            break
        else:
            print('Введите корректное значение')

    while True:
        employment = int(input('Выберите желаемый тип занятости (1 - полный день, 2 - неполный день, 3 - сменный график'
                               ' \n4 - частичная занятость, 5 - временная работа, 6 - вахтовый метод, 7 - стажировка):'))
        if employment == 1:
            employment = 'Полный рабочий день'
            break
        elif employment == 2:
            employment = 'Неполный рабочий день'
            break
        elif employment == 3:
            employment = 'Сменный график работы'
            break
        elif employment == 4:
            employment = 'Частичная занятость'
            break
        elif employment == 5:
            employment = 'Временная работа'
            break
        elif employment == 6:
            employment = 'Вахтовый метод'
            break
        elif employment == 7:
            employment = 'Стажировка'
            break
        else:
            print('Введите корректное значение')

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


def currency_filter(vacation_list, user_currency):
    """
    Фильтрует список вакансий оставляя вакансии только с зарплатой в валюте, указанной пользователем
    :param vacation_list: Список вакансий
    :param user_currency: Указанная пользователем валюта
    :return: Отфильтрованный список вакансий
    """
    filtered_list = []

    for vacation in vacation_list:
        if vacation['currency'].upper() == user_currency.upper():
            filtered_list.append(vacation)

    return filtered_list


def payment_filter(vacation_list, user_payment):
    """
    Фильтрует список вакансий, оставляя только подходящие пользователю по уровню ЗП
    :param vacation_list: Список вакансий
    :param user_payment: Указанная пользователем минимальную зарплату
    :return: Отфильтрованный список
    """

    filtered_list = []

    for vacancy in vacation_list:
        if vacancy['min_salary'] == 'Минимальная зарплата не указана' and \
                vacancy['max_salary'] == 'Максимальная зарплата не указана':
            continue
        elif vacancy['max_salary'].issubset(int):
            if user_payment < vacancy['max_salary']:
                filtered_list.append(vacancy)
            else:
                continue
        else:
            filtered_list.append(vacancy)

    return filtered_list


def experience_filter(vacation_list, user_experience):
    """
    Фильтрует список вакансий, оставляя только подходящие пользователю по опыту
    :param vacation_list: Список вакансий
    :param user_experience: Опыт пользователя
    :return: Отфильтрованный список вакансий
    """

    filtered_list = []

    for vacancy in vacation_list:
        if user_experience == 3:
            filtered_list.append(vacancy)
        elif user_experience == 2 and vacancy['experience'] != 'От 6 лет':
            filtered_list.append(vacancy)
        elif user_experience == 1 and (vacancy['experience'] == 'Без опыта' or vacancy['experience'] == 'От 1 года'):
            filtered_list.append(vacancy)
        elif user_experience == 0 and vacancy['experience'] == 'Без опыта':
            filtered_list.append(vacancy)
        else:
            continue

    return filtered_list


def employment_filter(vacation_list, user_employment):
    """
    Фильтрует список вакансий, оставляя только подходящие пользователю по типу занятости
    :param vacation_list: Список вакансий
    :param user_employment: Тип занятости, подходящий пользователю
    :return: Отфильтрованный список
    """

    filtered_list = []

    for vacancy in vacation_list:
        if vacancy['e']

def search_with_filters(keyword, platform):
    """
    Поиск вакансий по ключевому слову на заданной платформе с заданными фильтрами
    :param keyword: Ключевое слово
    :param platform: Номер платформы
    :return: Список вакансий
    """

    town, currency, payment, experience, employment = get_filters()

    if town != '':
        keyword += f' {town.lower().title()}'

    vacancies_data = search_without_filters(keyword, platform)
    filtered_vacancies = currency_filter(vacancies_data, currency)
    filtered_vacancies = payment_filter(filtered_vacancies, payment)
    filtered_vacancies = experience_filter(filtered_vacancies, experience)

    return filtered_vacancies


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

        data = search_with_filters(keyword, platform)

    elif filters.lower() == 'нет':

        data = search_without_filters(keyword, int(platform))

    vacancies = []

    for item in data:
        vacancy = Vacancy(item)
        vacancies.append(vacancy)

    return data, vacancies
