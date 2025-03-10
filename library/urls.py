from django.urls import path, include
from rest_framework_nested import routers

from .views import ShelfViewSet, PublisherViewSet, BookViewSet, LoanViewSet, FinePaymentViewSet, AuthorViewSet

router = routers.SimpleRouter()
router.register("shelves", ShelfViewSet)
router.register("authors", AuthorViewSet)
router.register("publishers", PublisherViewSet)
router.register("books", BookViewSet)
router.register("loans", LoanViewSet)

fine_payment_router = routers.NestedSimpleRouter(router, r"loans", lookup="loan")
fine_payment_router.register(r"fine-payments", FinePaymentViewSet, basename="loan-fine-payments")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(fine_payment_router.urls)),
]