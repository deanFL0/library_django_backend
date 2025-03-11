from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Book, Shelf, Loan, FinePayment, Publisher, Author
from .serializers import BookSerializer, ShelfSerializer, LoanSerializer, FinePaymentSerializer, PublisherSerializer, AuthorSerializer
from user.permissions import IsLibrarian, IsOwnerOrLibrarian
from .filters import ShelfFilter, AuthorFilter, PublisherFilter, BookFilter, LoanFilter

class ShelfViewSet(viewsets.ModelViewSet):
    queryset = Shelf.objects.all()
    serializer_class = ShelfSerializer
    permission_classes = [IsLibrarian]
    filterset_class = ShelfFilter

    @method_decorator(cache_page(60*10, key_prefix='shelf_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsLibrarian]
    filterset_class = AuthorFilter

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [IsLibrarian]
    filterset_class = PublisherFilter

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsLibrarian]
            
        return [permission() for permission in permission_classes]
    
    @method_decorator(cache_page(60*10, key_prefix='book_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        author_name = request.data.get("author")
        author, _ = Author.objects.get_or_create(name=author_name)

        publisher_name = request.data.get("publisher")
        publisher, _ = Publisher.objects.get_or_create(name=publisher_name, address="Unknown", phone="Unknown", email="Unknown")

        book_data = request.data.copy()
        book_data["author"] = author.author_id
        book_data["publisher"] = publisher.publisher_id

        serializer = self.get_serializer(data=book_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    filterset_class = LoanFilter

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsOwnerOrLibrarian]
        else:
            permission_classes = [IsLibrarian]
            
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action == 'list' and self.request.user.role == 'user':
            return Loan.objects.filter(user=self.request.user).prefetch_related('fine_payments')
        return Loan.objects.prefetch_related('fine_payments')
    
    @method_decorator(cache_page(60*10, key_prefix='loan_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        book = serializer.validated_data["book"]

        with transaction.atomic():
            book.refresh_from_db()
            borrowed_count = book.loans.filter(return_date__isnull=True).count()

            if borrowed_count >= book.available_copies:
                raise ValidationError("No available copies of this book")
            serializer.save()

class FinePaymentViewSet(viewsets.ModelViewSet):
    queryset = FinePayment.objects.all()
    serializer_class = FinePaymentSerializer
    permission_classes = [IsLibrarian]

    def get_queryset(self):
        return FinePayment.objects.filter(loan=self.kwargs["loan_pk"])

    def perform_create(self, serializer):
        loan = serializer.validated_data["loan"]
        loan.refresh_from_db()

        # add user uuid from loan to fine payment
        serializer.validated_data["user"] = loan.user

        if loan.is_paid:
            raise ValidationError("This loan has already been paid")
        
        loan.save()
        serializer.save()
    
    def update(self, request, *args, **kwargs):
        raise ValidationError("Method not allowed")
    
    def partial_update(self, request, *args, **kwargs):
        raise ValidationError("Method not allowed")
    
    def destroy(self, request, *args, **kwargs):
        raise ValidationError("Method not allowed")