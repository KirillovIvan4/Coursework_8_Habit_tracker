from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from users.tasks import check_user_is_active

class UserTestCase(APITestCase):
    def setUp(self):
        # Подготовка данных перед каждым теcтом
        self.user = User.objects.create(
            email='admin@admin.com',
            username='admin1235'
        )

    def test_user_create(self):
        url = reverse('users:register')
        data = {
            'email': 'new_user@example.com',  # Используем другой email
            'password': 'testpassword123',  # Добавляем обязательное поле password
            'username': 'Test12154',
        }
        response = self.client.post(url, data=data)

        print(response.json())  # Для отладки

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED,
            # Покажет ошибки валидации
            msg=f"Response data: {response.json()}"
        )
        self.assertEqual(
            User.objects.all().count(), 2
        )


class CheckUserActiveTaskTest(TestCase):
    def setUp(self):
        # Создаем тестовых пользователей
        self.current_time = timezone.now()

        # Активный пользователь, заходивший недавно
        self.active_user = User.objects.create(
            email='active@example.com',
            username='test1224',
            password='testpassword123',
            is_active=True,
            last_login=self.current_time - timedelta(days=10)
        )

        # Неактивный пользователь (не должен быть выбран)
        self.inactive_user = User.objects.create(
            email='inactive@example.com',
            username='test1225',
            password='testpassword123',
            is_active=False,
            last_login=self.current_time - timedelta(days=40))

        # Активный пользователь, который
        # не заходил больше месяца (должен быть выбран)
        self.to_deactivate_user = User.objects.create(
            email='to_deactivate@example.com',
            username='test1226',
            password='testpassword123',
            is_active=True,
            last_login=self.current_time - timedelta(days=35))

    def test_user_selection_logic(self):
        # Вызываем задачу напрямую (не как Celery task)
        check_user_is_active()

        # Проверяем, что правильный пользователь был деактивирован
        self.to_deactivate_user.refresh_from_db()
        self.active_user.refresh_from_db()
        self.inactive_user.refresh_from_db()

        self.assertFalse(self.to_deactivate_user.is_active)
        self.assertTrue(self.active_user.is_active)  # Не должен измениться
        self.assertFalse(self.inactive_user.is_active)  # Не должен измениться
