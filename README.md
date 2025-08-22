# Сервис для размещения учебных материалов на DjangoRestFramework
python manage.py runserver - запуск веб-приложения. Ctrl+C - остановка сервера.

python manage.py add_users - создание тестовых пользователей

python manage.py add_payments - создание тестовых оплат

http://127.0.0.1:8000/users/payments?ordering=-payment_date - в Postman сортировка оплат
по дате платежа в порядке убывания

http://127.0.0.1:8000/users/payments?ordering=payment_date - в Postman сортировка оплат
по дате платежа в порядке возрастания

http://127.0.0.1:8000/users/payments?paid_course=2 - в Postman фильтруем по оплаченному
курсу с id=2

http://127.0.0.1:8000/users/payments?paid_lesson=3 - в Postman фильтруем по оплаченному
уроку с id=3

http://127.0.0.1:8000/users/payments?payment_type=transfer - в Postman фильтруем по типу
оплаты transfer

## Описание:

Бэкенд веб-приложения для размещения учебных материалов. Описаны модели курсов,
уроков, пользователей, оплаты, настроены urls, написаны сериализаторы, CRUD для 
моделей курсов, уроков, оплаты. Созданы кастомные команды для наполнения базы данных
тестовыми пользователями и тестовыми оплатами. Для списка платежей настроена
фильтрация по курсу, по уроку, по способу оплаты, а также сортировка по дате оплаты.

## Требования к окружению:

Установите:
 - python 3.13.0
 - Poetry
 - Django
 - Pillow
 - python-dotenv
 - psycopg2 или psycopg2-binary
 - djangorestframework
 - django-filter
 - djangorestframework-simplejwt

В качестве базы данных используется PostgreSQL

## Установка:

1. Клонируйте репозиторий:
```
https://github.com/Bugrova-Irina/homework_30.1_drf/
```
2. Установите зависимости:
```
pip install -r requirements.txt
```
```
poetry shell
```
```
poetry add django
```
```
poetry add Pillow
```
```
poetry add psycopg2
```
```
poetry add python-dotenv
```
```
poetry add djangorestframework
```
```
poetry add django-filter
```
```
poetry add djangorestframework-simplejwt
```

## Использование:

После запуска сервера перейдите по ссылке http://127.0.0.1:8000/materials/.

## Тестирование:

Не реализовано

## Документация:

Нет дополнительной информации.

## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE)