# Сервис для размещения учебных материалов на DjangoRestFramework
```python manage.py runserver``` - запуск веб-приложения. Ctrl+C - остановка сервера.

```python manage.py createsuperadmin``` - создание суперпользователя

```python manage.py add_users``` - создание тестовых пользователей

```python manage.py add_payments``` - создание тестовых оплат

```python manage.py backup_data``` - выгрузка всех данных по курсам, урокам, пользователям
(без оплат) из БД в фикстуру в формате JSON. Сохраняется в папку backup.

Восстановить данные по курсам, урокам, пользователям из фикстуры:
```python manage.py loaddata backup/data.json```

```python manage.py test``` - запуск тестов

http://127.0.0.1:8000/materials/subscription/ - в Postman задайте метод POST и отправьте
запрос, например:
```
{
    "user": 2,
    "subscribe_course": "1",
    "status": "True"
}
```
Подписка на курс будет либо удалена, либо добавлена.

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

celery -A config worker -l INFO -P eventlet - запуск worker

celery -A config beat -l info -S django - запуск beat

## Описание:

Бэкенд веб-приложения для размещения учебных материалов. Описаны модели курсов,
уроков, пользователей, оплаты, настроены urls, написаны сериализаторы, CRUD для 
моделей курсов, уроков, оплаты. Созданы кастомные команды для наполнения базы данных
тестовыми пользователями и тестовыми оплатами. 

Для списка платежей настроена фильтрация по курсу, по уроку, по способу оплаты, 
а также сортировка по дате оплаты. Создана группа модераторов. Модераторы могут 
просматривать и обновлять курсы и уроки, но не могут их создавать и удалять. 

Добавлено поле "Владелец" в модели курса и урока. При создании курса или урока, 
ему автоматически присваивается владелец - авторизованный на данный момент пользователь.
Владелец может просматривать подробную информацию только о своих курсах или уроках, 
может их редактировать и удалять.

Реализована проверка ссылок на видео в уроке на отсутствие любых доменов, кроме YouTube.
В описание курса добавлен признак "подписка", который указывает на то, что пользователь
подписан на обновления курса или нет.

Добавлено тестирование корректности работы CRUD уроков и функционала работы подписки
на обновления курса. Добавлен отчет о покрытии тестами в папке htmlcov/index.html.

Для проекта подключен и настроен вывод документации с помощью drf-yasg.

Настроена возможность оплаты курсов и уроков с помощью сервиса stripe.com. Чтобы 
получить ссылку на оплату, авторизуйтесь в Postman http://127.0.0.1:8000/users/login/, 
заберите полученный токен, авторизуйтесь с его помощью на странице Postman
http://127.0.0.1:8000/users/payments/ и отправьте POST запрос с оплатой урока или круса
в формате:
{
    "user": 6,
    "paid_course": 2,
    "amount": 5000
}
В полученном ответе в поле "link" скопируйте ссылку и откройте ее в браузере, откроется
страница оплаты.

Добавлена рассылка писем об обновлении курсов, на которые они подписаны, с расписанием - 
1 раз в день. Письмо приходит в случае если обновлен курс или уроки, входящие в его состав.
Для проверки работы отправки писем запустите worker, beat, сделайте активной подписку
у пользователя на какой-нибудь курс, внесите изменения в этот курс и/или урок, входящий в
состав этого курса, измените в settings.py настройку "schedule": timedelta(days=1) на 
"schedule": timedelta(minutes=1) и дождитесь письма.

Создана фоновая задача, которая проверяет пользователей по дате последнего входа по полю 
last_login  и, если пользователь не заходил более месяца, или создан более месяца назад и 
никогда не заходил на сайт, то он блокируется с помощью флага is_active (становится 
неактивным).


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
 - flake8
 - black
 - isort
 - coverage
 - drf-yasg
 - stripe
 - forex-python
 - celery
 - django-celery-beat
 - eventlet (для Windows)

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
```
poetry add flake8
```
```
poetry add black
```
```
poetry add isort
```
```
poetry add coverage
```
```
poetry add drf-yasg
```
```
poetry add stripe
```
```
poetry add forex-python
```
```
poetry add redis
```
```
poetry add celery
```
```
poetry add django-celery-beat
```
```
poetry add eventlet
```
3. Запустите Redis

## Использование:

После запуска сервера перейдите по ссылке http://127.0.0.1:8000/materials/.

### Запуск проекта с использованием Docker Compose:
В корне проекта должны быть файлы:
- Dockerfile
- docker-compose.yml
- .env (создайте на основе .env.sample со своими значениями)

#### Команды для запуска:
Выполните сборку образов:
```
docker-compose build
```

Запуск контейнеров в фоновом режиме:
```
docker-compose up -d
```

Убедитесь, что все контейнеры запущены:
```
docker-compose ps
```

Примените миграции базы данных:
```
docker-compose exec web python manage.py migrate
```

Создайте учетную запись администратора
```
docker-compose exec web python manage.py createsuperadmin
```

Проверка работы приложения:
Перейдите по адресу: http://localhost:8002/materials/lessons/

#### Проверка работоспособности сервисов
1. Веб-сервис (Django). Откройте в браузере http://localhost:8002/ или выполните команду:
```
curl -X GET http://localhost:8002/materials/lessons/
```
2. База данных (PostgreSQL):
```
docker-compose exec db psql -U your_database_user -d your_database_name -c "\dt"
```
Результат: должен отобразить список таблиц в базе данных.

3. Redis:
```
docker-compose exec redis redis-cli ping
```
Результат: должен вернуть PONG.

4. Celery Worker:
```
docker-compose logs celery
```
Результат: в логах должны быть сообщения об успешном запуске worker.

5. Celery Beat:
```
docker-compose logs beat
```
Результат: в логах должны быть сообщения о запуске планировщика.

6. Административная панель Django:
Откройте в браузере http://localhost:8002/admin/

7. Остановка контейнеров:
```
docker-compose down
```
8. Перезапуск с пересборкой образов:
```
docker-compose up -d --build
```
Просмотр логов конкретного сервиса (web, db, redis, celery, beat):
```
docker-compose logs [service_name]
```

## Тестирование:

Добавлено тестирование корректности работы CRUD уроков и функционала работы подписки
на обновления курса. Добавлен отчет о покрытии тестами в папке htmlcov/index.html.

## Документация:

Для проекта подключен и настроен вывод документации с помощью drf-yasg.

## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE)