from django.urls import path
from rest_framework import routers

from .views import ShelfViewSet, PublisherViewSet, BookViewSet

router = routers.DefaultRouter()
router.register("shelves", ShelfViewSet)
router.register("publishers", PublisherViewSet)
router.register("books", BookViewSet)

urlpatterns = router.urls