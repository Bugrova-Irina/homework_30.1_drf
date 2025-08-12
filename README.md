# Сервис для размещения учебных материалов на DjangoRestFramework
python manage.py runserver - запуск веб-приложения. Ctrl+C - остановка сервера.

## Описание:

Бэкенд веб-приложения для размещения учебных материалов.

## Требования к окружению:

Установите:
 - python 3.13.0
 - Poetry
 - Django
 - Pillow
 - python-dotenv
 - psycopg2 или psycopg2-binary
 - djangorestframework

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

## Использование:

После запуска сервера перейдите по ссылке http://127.0.0.1:8000/materials/.

## Тестирование:

Не реализовано

## Документация:

Нет дополнительной информации.

## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE)