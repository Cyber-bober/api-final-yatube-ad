# Yatube API

API для социальной сети Yatube. Позволяет создавать публикации, комментировать их, подписываться на других пользователей и получать информацию о группах.

## Установка

Клонируйте репозиторий, установите зависимости, примените миграции и запустите сервер:
   ```bash
   git clone https://github.com/your-username/yatube-api.git
   cd yatube-api

   pip install -r requirements.txt

   python manage.py makemigrations posts
   python manage.py migrate

   python manage.py runserver
   ```
   Откройте документацию: http://127.0.0.1:8000/redoc/
