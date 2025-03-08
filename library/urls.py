from django.urls import path
from rest_framework import routers

from .views import ShelfViewSet, PublisherViewSet, BookViewSet, LoanViewSet

router = routers.DefaultRouter()
router.register("shelves", ShelfViewSet)
router.register("publishers", PublisherViewSet)
router.register("books", BookViewSet)
router.register("loans", LoanViewSet)

urlpatterns = router.urls