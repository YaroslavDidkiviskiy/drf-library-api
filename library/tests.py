from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from library.models import Book, Borrowing

User = get_user_model()


class BorrowingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@user.com',
            password='testpass'
        )
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            inventory=3,
            cover='HARD',
            daily_fee=9.99
        )
        self.borrowing_data = {
            'book': self.book.id,
            'user': self.user.id,
            'expected_return_date': '2023-12-31'
        }
        self.client.force_authenticate(user=self.user)
        self.base_url = "/api/library/borrowings/"

    def test_create_borrowing(self):
        """Тест створення позички та зменшення інвентарю"""
        response = self.client.post(
            self.base_url,
            data=self.borrowing_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 2)

        borrowing = Borrowing.objects.get(id=response.data['id'])
        self.assertEqual(borrowing.book.id, self.book.id)
        self.assertIsNone(borrowing.actual_return_date)

    def test_return_book(self):
        """Тест повернення книжки та збільшення інвентарю"""
        # Створюємо позичку через API
        create_response = self.client.post(
            self.base_url,
            data=self.borrowing_data,
            format='json'
        )
        borrowing_id = create_response.data['id']

        # Повертаємо книжку
        return_url = f"{self.base_url}{borrowing_id}/return/"
        response = self.client.post(return_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 3)  # Повертаємо до початкового значення

        borrowing = Borrowing.objects.get(id=borrowing_id)
        self.assertEqual(borrowing.actual_return_date, timezone.now().date())

    def test_return_already_returned_book(self):
        """Тест неможливості повернути вже повернуту книжку"""
        # Створюємо позичку через API
        create_response = self.client.post(
            self.base_url,
            data=self.borrowing_data,
            format='json'
        )
        borrowing_id = create_response.data['id']

        # Повертаємо книжку вперше
        return_url = f"{self.base_url}{borrowing_id}/return/"
        self.client.post(return_url)

        # Спроба повернути вдруге
        response = self.client.post(return_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Ця книжка вже була повернена')

    def test_serializer_selection(self):
        """Тест вибору правильного серіалізатора"""
        # Створюємо позичку через API
        create_response = self.client.post(
            self.base_url,
            data=self.borrowing_data,
            format='json'
        )
        borrowing_id = create_response.data['id']

        # Перевіряємо список
        list_response = self.client.get(self.base_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)

        # Перевіряємо детальний перегляд
        detail_url = f"{self.base_url}{borrowing_id}/"
        detail_response = self.client.get(detail_url)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)

        # Перевіряємо створення
        create_response = self.client.post(self.base_url, data=self.borrowing_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
