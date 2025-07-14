from django.db import transaction
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from library.models import Book, Borrowing
from library.serializers import BookSerializer, BorrowingSerializer, BorrowingDetailSerializer, BorrowingListSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = ()


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all().select_related("book", "user")
    permission_classes = ()

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        return BorrowingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book = serializer.validated_data['book']

        if book.inventory < 1:
            return Response(
                {"error": "Ця книжка недоступна для позичання"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            book.inventory -= 1
            book.save(update_fields=['inventory'])
            borrowing = serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(
        detail=True,
        methods=['post'],
        url_path='return',
        permission_classes=()
    )
    def return_book(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            return Response(
                {"error": "Ця книжка вже була повернена"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            book = borrowing.book
            book.inventory += 1
            book.save(update_fields=['inventory'])

            borrowing.actual_return_date = timezone.now().date()
            borrowing.save(update_fields=['actual_return_date'])

        serializer = self.get_serializer(borrowing)
        return Response(serializer.data)
