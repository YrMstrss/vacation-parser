from func import interaction_with_user, compare_interactions
from vacancy import write_info_to_json


def main():
    vacancies = interaction_with_user()

    if vacancies:
        vacancy_list = []
        dict_list = []

        for vacancy in vacancies:
            vacancy_dict = vacancy.make_dict()
            vacancy_list.append(vacancy)
            dict_list.append(vacancy_dict)
            print(vacancy_dict)

        print(compare_interactions(vacancy_list))

        print('Результаты будут записаны в файл "search_results.json"')

        write_info_to_json(vacancy_dict)
    else:
        print('Вакансии по вашему запросу не найдены')


if __name__ == '__main__':
    main()
