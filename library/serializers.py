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

class LoanSerializer(serializers.ModelSerializer):
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = Loan
        fields = (
            "loan_id",
            "loan_date",
            "due_date",
            "return_date",
            "status",
            "fine_amount",
            "book",
            "user",
            "is_overdue",
            "created_at",
        )
        read_only_fields = ("loan_id", "fine_amount", "is_overdue", "created_at")

class FinePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinePayment
        fields = (
            "payment_id",
            "loan",
            "amount",
            "payment_date",
        )
        read_only_fields = ("payment_id",)