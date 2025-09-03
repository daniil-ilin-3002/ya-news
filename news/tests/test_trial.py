from django.test import TestCase
import unittest
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
# Импортируем модель, чтобы работать с ней в тестах.
from news.models import News


@unittest.skip("Временный пропуск: не мешать работе.")
# Создаём тестовый класс с произвольным названием, наследуем его от TestCase.
class TestNews(TestCase):

    # В методе класса setUpTestData создаём тестовые объекты.
    # Оборачиваем метод соответствующим декоратором.
    @classmethod
    def setUpTestData(cls):
        # Стандартным методом Django ORM create() создаём объект класса.
        # Присваиваем объект атрибуту класса: назовём его news.
        cls.news = News.objects.create(
            title='Заголовок новости',
            text='Тестовый текст',
        )

    # Проверим, что объект действительно был создан.
    def test_successful_creation(self):
        # При помощи обычного ORM-метода посчитаем количество записей в базе.
        news_count = News.objects.count()
        # Сравним полученное число с единицей.
        self.assertEqual(news_count, 1)

    def test_title(self):
        # Сравним свойство объекта и ожидаемое значение.
        self.assertEqual(self.news.title, 'Заголовок новости')


# Получаем модель пользователя.
User = get_user_model()


@unittest.skip("Временный пропуск: не мешать работе.")
class TestNews(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаём пользователя.
        cls.user = User.objects.create(username='testUser')
        # Создаём объект клиента.
        cls.user_client = Client()
        # "Логинимся" в клиенте при помощи метода force_login().
        cls.user_client.force_login(cls.user)
        # Теперь через этот клиент можно отправлять запросы
        # от имени пользователя с логином "testUser".
