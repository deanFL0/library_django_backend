from rest_framework import serializers

from .models import Book, Shelf, Loan, FinePayment, Publisher, Author

class ShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelf
        fields = (
            "shelf_id",
            "name",
            "description",
        )
        read_only_fields = ("shelf_id",)

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = (
            "author_id",
            "name",
        )
        read_only_fields = ("author_id",)

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = (
            "publisher_id",
            "name",
            "address",
            "phone",
            "email",
        )
        read_only_fields = ("publisher_id",)
    
class BookSerializer(serializers.ModelSerializer):
    available_copies = serializers.ReadOnlyField()
    
    class Meta:
        model = Book
        fields = (
            "book_id",
            "book_img",
            "title",
            "author",
            "publisher",
            "publication_date",
            "isbn",
            "copies",
            "shelf",
            "available_copies",
        )
        read_only_fields = ("book_id", "available_copies")

class FinePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinePayment
        fields = (
            "payment_id",
            "amount_paid",
            "payment_date",
            "loan",
            "user",
        )
        read_only_fields = ("payment_id", "payment_date", "user",)

class LoanSerializer(serializers.ModelSerializer):
    is_overdue = serializers.ReadOnlyField()
    fine_payments = FinePaymentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Loan
        fields = (
            "loan_id",
            "loan_date",
            "due_date",
            "return_date",
            "status",
            "fine_amount",
            "is_paid",
            "book",
            "user",
            "is_overdue",
            "created_at",
            "fine_payments",
        )
        read_only_fields = ("loan_id", "loan_date", "fine_amount", "is_paid", "is_overdue", "created_at")