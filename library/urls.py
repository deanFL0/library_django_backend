from django.urls import path
from rest_framework import routers

from .views import ShelfViewSet, PublisherViewSet, BookViewSet, LoanViewSet, FinePaymentViewSet, AuthorViewSet

router = routers.DefaultRouter()
router.register("shelves", ShelfViewSet)
router.register("authors", AuthorViewSet)
router.register("publishers", PublisherViewSet)
router.register("books", BookViewSet)
router.register("loans", LoanViewSet)
router.register("fine-payments", FinePaymentViewSet)

urlpatterns = router.urls