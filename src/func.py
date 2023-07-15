from API_classes import HeadHunter_API, SuperJob_API
from vacancy import Vacancy


def get_filters() -> tuple:
    print('Для пропуска нежелательных фильтров нажмите Enter')

    town = input('В каком городе ищем вакансии?\n')

    currency = input('Введите желаемую валюту (RUB, USD, EUR): \n')

    if currency != "":
        payment = input('Введите минимальную желаемую заработную плату: \n')
    else:
        payment = ""

    while True:
        experience = input('Ваш опыт работы (0 - без опыта, 1 - от 1 до 3 лет, 2 - от 3 до 6 лет, '
                           '3 - более 6 лет): \n')
        if experience == '0' or experience == '1' or experience == '2' or experience == '3' or experience == '':
            break
        else:
            print('Введите корректное значение')

    while True:
        employment = input('Выберите желаемый тип занятости (1 - полный день, 2 - неполный день, 3 - сменный график'
                           ' \n4 - частичная занятость, 5 - временная работа, 6 - вахтовый метод, 7 - стажировка):\n')
        if employment == '1':
            employment = 'Полный рабочий день'
            break
        elif employment == '2':
            employment = 'Неполный рабочий день'
            break
        elif employment == '3':
            employment = 'Сменный график работы'
            break
        elif employment == '4':
            employment = 'Частичная занятость'
            break
        elif employment == '5':
            employment = 'Временная работа'
            break
        elif employment == '6':
            employment = 'Вахтовый метод'
            break
        elif employment == '7':
            employment = 'Стажировка'
            break
        elif employment == '':
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

    vacancies = []

    for item in vacancies_data:
        vacancy = Vacancy(item)
        vacancies.append(vacancy)

    return vacancies


def currency_filter(vacation_list, user_currency):
    """
    Фильтрует список вакансий оставляя вакансии только с зарплатой в валюте, указанной пользователем
    :param vacation_list: Список вакансий
    :param user_currency: Указанная пользователем валюта
    :return: Отфильтрованный список вакансий
    """
    filtered_list = []

    for vacation in vacation_list:
        if vacation.currency.upper() == user_currency.upper():
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
        if vacancy.min_salary == 'Минимальная зарплата не указана' and \
                vacancy.max_salary == 'Максимальная зарплата не указана':
            continue
        elif type(vacancy.max_salary) is int:
            if int(user_payment) < int(vacancy.max_salary):
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
        if user_experience == '3':
            filtered_list.append(vacancy)
        elif user_experience == '2' and vacancy.experience != 'От 6 лет':
            filtered_list.append(vacancy)
        elif user_experience == '1' and (vacancy.experience == 'Без опыта' or vacancy.experience == 'От 1 года'):
            filtered_list.append(vacancy)
        elif user_experience == '0' and vacancy.experience == 'Без опыта':
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
        if vacancy.employment == user_employment:
            filtered_list.append(vacancy)

    return filtered_list


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

    vacancies_data = search_without_filters(keyword, int(platform))
    if currency != '':
        vacancies_data = currency_filter(vacancies_data, currency)
    if payment != '':
        vacancies_data = payment_filter(vacancies_data, payment)
    if experience != '':
        vacancies_data = experience_filter(vacancies_data, experience)
    if employment != '':
        vacancies_data = employment_filter(vacancies_data, employment)

    return vacancies_data


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

    return data


def compare_vacancies(vacancies_list: list, first_name: str, second_name: str):
    """
    Находит в списке вакансий вакансии, выбранные пользователем и сравнивает их по минимальной ЗП
    :param vacancies_list: Список вакансий
    :param first_name: Название первой вакансии
    :param second_name: Название второй вакансии
    :return: string - результат сравнения вакансий
    """

    for vacancy in vacancies_list:
        if vacancy.name == first_name:
            first_vacancy = vacancy
        if vacancy.name == second_name:
            second_vacancy = vacancy

    try:
        if first_vacancy >= second_vacancy:
            return f'Заработная плата у вакансии "{first_vacancy.name}" выше, чем у "{second_vacancy.name}"'
        return f'Заработная плата у вакансии "{first_vacancy.name}" ниже, чем у "{second_vacancy.name}"'
    except ValueError:
        return 'Невозможно провести сравнение'


def compare_interactions(vacancy_list: list):
    """
    Получает у пользователя информацию о названиях вакансий, которые необходимо сравнить и вызывает функцию сравнения
    :param vacancy_list: Список вакансий
    :return: Строка, сообщающая информацию о результате выполнения функции
    """
    comparison = input('Хотите сравнить какие-то вакансии по уровню ЗП?\n')

    if comparison.lower() == 'да':
        while True:
            print('Для выхода из сравнения напишите: СТОП')
            first_vacancy_name = input('Введите название первой вакансии для сравнения:\n')
            second_vacancy_name = input('Введите название второй вакансии для сравнения:\n')

            if first_vacancy_name.lower() == 'стоп' or second_vacancy_name.lower() == 'стоп':
                return 'Готово'
            else:
                print(compare_vacancies(vacancy_list, first_vacancy_name, second_vacancy_name))
    else:
        return 'Готово'
