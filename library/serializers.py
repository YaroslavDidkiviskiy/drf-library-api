from rest_framework import serializers

from user.serializers import UserSerializer
from .models import Book, Borrowing


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee")


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "book", "user", "borrow_date", "expected_return_date", "actual_return_date")

    def validate_book(self, value):
        if value.inventory < 1:
            raise serializers.ValidationError("Ця книжка недоступна")
        return value


class BorrowingListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="email")
    book = serializers.SlugRelatedField(read_only=True, slug_field="title")

    class Meta:
        model = Borrowing
        fields = ("id", "book", "user", "expected_return_date", "actual_return_date")


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    user = UserSerializer()

    class Meta:
        model = Borrowing
        fields = ("id", "book", "user", "expected_return_date", "actual_return_date")

