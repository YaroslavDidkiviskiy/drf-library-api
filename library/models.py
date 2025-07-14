from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError


class Book(models.Model):
    STATUS_CHOICES = [
        ("Hard", "HARD"),
        ("Soft", "SOFT"),
    ]
    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=255, choices=STATUS_CHOICES, default="Hard")
    inventory = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.title}, {self.author}, {self.daily_fee}$, {self.inventory}"


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrowings")

    def clean(self):
        if self.actual_return_date and self.actual_return_date < self.borrow_date:
            raise ValidationError("Дата повернення не може бути раніше дати позичання")

        if self.actual_return_date and self.pk:
            original = Borrowing.objects.get(pk=self.pk)
            if original.actual_return_date:
                raise ValidationError("Не можна змінювати дату повернення для вже поверненої книжки")

    def __str__(self):
        return f"{self.book.title}, {self.borrow_date} - {self.expected_return_date}, {self.actual_return_date}"

