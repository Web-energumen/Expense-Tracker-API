from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Expense

User = get_user_model()


class ExpenseAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='34qwerty1234')
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.expense_data = {
            'title': 'Test Expense',
            'amount': 100,
            'note': 'Test Note',
            'category': 'groceries',
            'date': date.today(),
        }

    def test_create_expense(self):
        Expense.objects.create(user=self.user, **self.expense_data)
        url = reverse('expense-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(Expense.objects.get().title, 'Test Expense')

    def test_list_expense(self):
        Expense.objects.create(user=self.user, **self.expense_data)
        url = reverse('expense-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_expense(self):
        expense = Expense.objects.create(user=self.user, **self.expense_data)
        url = reverse('expense-detail', kwargs={'pk': expense.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expense.refresh_from_db()
        self.assertEqual(str(expense.amount), '100.00')

    def test_delete_expense(self):
        expense = Expense.objects.create(user=self.user, **self.expense_data)
        url = reverse('expense-detail', kwargs={'pk': expense.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Expense.objects.count(), 0)

    def test_authentication_required(self):
        self.client.credentials()
        url = reverse('expense-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ExpenseFilterTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', password='34qwerty1234'
        )
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        today = date.today()
        self.expenses = [
            Expense.objects.create(user=self.user, title='Grocery 1', amount=10, category='groceries', date=today),
            Expense.objects.create(user=self.user, title='Grocery 2', amount=20, category='groceries',
                                   date=today - timedelta(days=5)),
            Expense.objects.create(user=self.user, title='Leisure 1', amount=30, category='leisure',
                                   date=today - timedelta(days=30)),
            Expense.objects.create(user=self.user, title='Electronics', amount=40, category='electronics',
                                   date=today - timedelta(days=80)),
        ]

    def test_filter_by_date_range_past_week(self):
        url = reverse('expense-list')
        response = self.client.get(url, {'date_range': 'past_week'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_date_range_past_month(self):
        url = reverse('expense-list')
        response = self.client.get(url, {'date_range': 'past_month'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_by_date_range_last_3_months(self):
        url = reverse('expense-list')
        response = self.client.get(url, {'date_range': 'last_3_months'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_filter_by_start_and_end_date(self):
        start_date = (date.today() - timedelta(days=10)).isoformat()
        end_date = date.today().isoformat()
        url = reverse('expense-list')
        response = self.client.get(url, {'start_date': start_date, 'end_date': end_date})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_category(self):
        url = reverse('expense-list')
        response = self.client.get(url, {'category': 'groceries'})

        self.assertEqual(len(response.data), 2)
        for expense in response.data:
            self.assertEqual(expense['category'], 'groceries')
