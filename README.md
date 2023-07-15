# **Vacation parser** 

Программа предназначена для поиска по ключевому слову вакансий на платформах HeadHunter и SuperJob (далее по тексту 
HH и SJ, соответственно).

*Количество результатов, получаемых с каждого из сайтов, 100.

## API_classes.py

Файл содержит классы, необходимые для подключения к HH и SJ при помощи API.

## vacancy.py

Файл содержит класс вакансии, инициализирующий по полученным при помощи API данным каждую вакансию. 
Данный класс имеет метод позволяющий сравнить 2 вакансии по минимальному 
уровню заработной платы, а так же метод, возвращающий данные о вакансии в json-подобном
формате.

Так же файл _vacancy.py_ включает в себя функцию, записывающую полученную о вакансиях информацию в 
json-файл. 

## func.py

В файле хранятся функции, необходимые для взаимодействия с пользователем (получение информации о ключевом 
слове, информации о необходимых пользователю фильтрах), функции, необходимые для фильтрации полученных результатов, и
функции, необходимые для реализации сравнения выбранных пользователем вакансий.

## Работа программы

Для выполнения программы запускается файл _main.py_. 

Чтобы была возможность выполнять поиск вакансий на SJ необходимо получить API-ключ.

### Получение API-ключа SJ:

1. Необходимо зарегистрироваться на сайте SJ.

> https://superjob.ru/

2. Заполнить заявку на приложение (допускается заполнить поля произвольной информацией)

>https://api.superjob.ru/

3. Посмотреть полученный API-ключ можно по ссылке (поле "Secret key"):

> https://api.superjob.ru/info/

4. Установить полученный ключ в переменные среды