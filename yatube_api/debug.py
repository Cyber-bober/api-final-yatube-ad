import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yatube_api.settings')
django.setup()

from django.contrib.auth.models import User
from posts.models import Follow

# Создаем пользователей
user1 = User.objects.create_user(username='TestUser')
user2 = User.objects.create_user(username='TestUser2')
user3 = User.objects.create_user(username='TestUserAnother')

# Создаем подписки как в тесте
Follow.objects.create(user=user1, following=user3)  # follow_1
Follow.objects.create(user=user2, following=user1)  # follow_2
Follow.objects.create(user=user2, following=user3)  # follow_3
Follow.objects.create(user=user3, following=user1)  # follow_4
Follow.objects.create(user=user1, following=user2)  # follow_5

print("=== ВСЕ ПОДПИСКИ ===")
for f in Follow.objects.all():
    print(f"ID: {f.id}, user: {f.user.username}, following: {f.following.username}")

print("\n=== ПОДПИСКИ ДЛЯ TestUser (user=user1) ===")
user_follows = Follow.objects.filter(user=user1)
print(f"Всего: {user_follows.count()}")
for f in user_follows:
    print(f"ID: {f.id}, user: {f.user.username}, following: {f.following.username}")

print("\n=== ФИЛЬТР following=TestUser2 ===")
filtered = user_follows.filter(following=user2)
print(f"Найдено: {filtered.count()}")
for f in filtered:
    print(f"ID: {f.id}, user: {f.user.username}, following: {f.following.username}")

print("\n=== ФИЛЬТР ПО following__username ===")
filtered_by_username = user_follows.filter(following__username='TestUser2')
print(f"Найдено: {filtered_by_username.count()}")
for f in filtered_by_username:
    print(f"ID: {f.id}, user: {f.user.username}, following: {f.following.username}")