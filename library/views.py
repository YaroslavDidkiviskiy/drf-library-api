from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.viewsets import ViewSet

from library.models import Book
from library.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = ()
