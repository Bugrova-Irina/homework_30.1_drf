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

## Настройка удаленного сервера и деплоя
1. Установите Python 3.13.
2. Установите Django версии 3.2.
3. Установите Gunicorn и Nginx для обработки запросов.

#### Подключение к серверу:
```
ssh username@server_ip
```

#### Обновление системы:
```
sudo apt update && sudo apt upgrade -y
```

#### Установка базовых пакетов:
```
sudo apt install -y curl wget git htop nano ufw
```

#### Настройка брандмауэра:
```
sudo ufw allow ssh
```
```
sudo ufw allow 80
```
```
sudo ufw allow 443
```
```
sudo ufw enable
```

### Настройка сервера
1. Настройте SSH-доступ с использованием SSH-ключей для повышения безопасности.
2. Закройте все ненужные порты, оставив открытыми только те, которые необходимы (например, 80 для HTTP и 443 для HTTPS).
3. Установите и настройте Supervisor для автоматического перезапуска приложения при изменениях.

### Создание пользователя для деплоя
Создание пользователя
```
sudo adduser deployer
```
```
sudo usermod -aG sudo deployer
```

Настройка SSH-доступа
```
sudo mkdir /home/deployer/.ssh
```
```
sudo cp ~/.ssh/authorized_keys /home/deployer/.ssh/
```
```
sudo chown -R deployer:deployer /home/deployer/.ssh
```
```
sudo chmod 700 /home/deployer/.ssh
```
```
sudo chmod 600 /home/deployer/.ssh/authorized_keys
```

### Настройка Docker и Docker Compose
#### Установка Docker
```
curl -fsSL https://get.docker.com -o get-docker.sh
```
```
sudo sh get-docker.sh
```
#### Добавление пользователя в группу docker
```
sudo usermod -aG docker $USER
```
```
sudo usermod -aG docker deployer
```
#### Перезагрузка сессии
```
newgrp docker
```
#### Проверка установки
```
docker --version
```
#### Установка Docker Compose
#### Скачивание последней версии
```
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
#### Назначение прав
```
sudo chmod +x /usr/local/bin/docker-compose
```
#### Проверка установки
```
docker-compose --version
```
### Деплой
1. Склонируйте репозиторий на сервер.
2. Выполните миграции базы данных с помощью команды python manage.py migrate.
3. Запустите сервер с помощью Gunicorn: gunicorn myproject.wsgi:application.
4. Настройте Nginx для проксирования запросов к Gunicorn.

### Выполните на сервере команды:
На сервере настроен systemd для автоматического управления.
#### Создание systemd сервиса
```
sudo nano /etc/systemd/system/myapp.service
```

Приложение будет автоматически запускаться и перезапускаться при изменениях или сбоях
```
sudo systemctl daemon-reload
```
```
sudo systemctl restart myapp.service
```
```
sudo systemctl status myapp.service
```
Удаленный сервер может автоматически перезагружать приложение при внесении изменений.
Workflow запускается при каждом push в репозиторий. Проект автоматически деплоится 
на удаленный сервер. Все чувствительные данные вынесены в переменные окружения и 
подключены к workflow через Secrets GitHub. В secrets and variables задайте секреты

DEPLOY_DIR
DOCKER_HUB_ACCESS_TOKEN
DOCKER_HUB_USERNAME
SECRET_KEY
SERVER_IP
SSH_KEY
SSH_USER

Проверьте работу приложения по адресу http://your_server_name/materials/

#### команды для мониторинга работы приложения на сервере
#### Статус приложения
```
sudo systemctl status myapp.service
```
#### Логи приложения
```
sudo journalctl -u myapp.service -f
```
#### Логи Docker контейнера
```
docker logs myapp
```
#### Использование ресурсов
```
docker stats myapp
```
#### Проверка сети
```
sudo netstat -tulpn | grep :80
```
#### Проверка доступности
```
curl -I http://localhost/
```

## Тестирование:

Добавлено тестирование корректности работы CRUD уроков и функционала работы подписки
на обновления курса. Добавлен отчет о покрытии тестами в папке htmlcov/index.html.

## Документация:

Для проекта подключен и настроен вывод документации с помощью drf-yasg.

## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE)