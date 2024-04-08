# 'Хакатон Vink х Практикум март-апрель’24'

### Задача
Разработать и внедрить чат-бота с технологией GPT
на сайт компании для предоставления консультаций по материалам и
оборудованию, а также оказания помощи клиентам 24/7.


### Команда

[Максим Савилов - developer](https://github.com/msavilov)

[Андрей Догадкин - developer](https://github.com/AndreyDogadkin)

### Технологии
- _[Python 3.11.6](https://www.python.org/downloads/release/python-3116/)_
- _[Django 4.2](https://www.djangoproject.com/download/4.2.11/tarball/)_
- _[Django Rest Framework](https://pypi.org/project/djangorestframework/)_
- _[Postgresql 15](https://hub.docker.com/_/postgres)_  Docker-образ
- _[Docker and docker-compose](https://www.docker.com/get-started/)_
- _[YandexGPT](https://cloud.yandex.ru/ru/docs/yandexgpt/quickstart#console_1)_
- _[pyTelegramBotAPI]()_

### Быстрый старт.
* В терминале (командной строке):
    ```bash
    git clone https://github.com/hackathon-Vink-Team-3/chat-bot-backend.git
    ```
* В терминале (командной строке):
    ```bash
    cd chat-bot-backend
    ```
* Cоздать файл `.env` в соответствии с шаблоном `.env.example`.
* Перейти в директорию .docker `cd .docker`
* Выполнить команду `docker compose up`


### Инструкция по запуску в dev режиме.
**Без докера**
#### 1. Клонировать репозиторий.
В терминале (командной строке):
```bash
git clone https://github.com/hackathon-Vink-Team-3/chat-bot-backend.git
```

#### 2. Перейти в корневой каталог приложения.
В терминале (командной строке):
```bash
cd chat-bot-backend
```

#### 3. Создать и активировать виртуальное окружение
В терминале в корневом каталоге приложения, находясь chat-bot-backend:
```bash
# Создать виртуальное окружение
python -m venv venv
```

#### 4. Активировать виртуальное окружение для проекта
```bash
# Если Windows:
source venv\Script\activate

# Если Linux или Mac
source venv\bin\activate
```

#### 5. В активированном виртуальном окружении необходимо обновить менеджер пакетов pip и установить зависимости:
```bash
python -m pip install --upgrade pip
pip install -r ./chat-bot/requirements.txt
```

#### 6. Далее нужно подготовить проект к запуску.
В корневом каталоге chat-bot-backend создать файл `.env` в соответствии с
шаблоном `.env.example`.

Переименовать файл `_local_settings` в `local_settings` для переопределения некоторых констант.


#### 7. Выполнить миграции на уровне проекта из директории `/chat-bot/`:

   ```bash
   # для OS Lunix и MacOS
   python3 manage.py makemigrations && python3 manage.py migrate

   # для OS Windows
   python manage.py makemigrations && python manage.py migrate
   ```

#### 8. Запустить redis:
   ```bash
   # для MacOS
   brew services start redis
   ```

#### 9. Запуск проекта локально:

   ```bash
   # для OS Lunix и MacOS
   python3 manage.py runserver

   # для OS Windows
   python manage.py runserver
   ```

### Работа с документацией
- [Swagger](https://vink-chat.ddns.net/api/v1/swagger)
- [Redoc](https://vink-chat.ddns.net/api/v1/redoc)