from API_classes import HeadHunter_API, SuperJob_API


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

