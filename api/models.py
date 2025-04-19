from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Expense(models.Model):
    CATEGORY_CHOICES = (
        ('groceries', 'Groceries'),
        ('leisure', 'Leisure'),
        ('electronics', 'Electronics'),
        ('utilities', 'Utilities'),
        ('clothing', 'Clothing'),
        ('health', 'Health'),
        ('others', 'Others'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    note = models.TextField(blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    date = models.DateField(auto_now_add=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.amount}'

