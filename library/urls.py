from django.urls import path, include
from rest_framework import routers
from .views import BookViewSet, BorrowingViewSet


app_name = "library"

router = routers.DefaultRouter()
router.register("books", BookViewSet, basename="book")
router.register("borrowings", BorrowingViewSet, basename="borrowing")

urlpatterns = [
    path("", include(router.urls)),
]
