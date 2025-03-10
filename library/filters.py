import django_filters

from .models import Book, Shelf, Loan, FinePayment, Publisher, Author

class ShelfFilter(django_filters.FilterSet):
    class Meta:
        model = Shelf
        fields = {
            "name": ["exact", "icontains"],
        }

class AuthorFilter(django_filters.FilterSet):
    class Meta:
        model = Author
        fields = {
            "name": ["exact", "icontains"]
        }

class PublisherFilter(django_filters.FilterSet):
    class Meta:
        model = Publisher
        fields = {
            "name": ["exact", "icontains"],
            "email": ["exact", "icontains"],
        }

class BookFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(field_name="author__name", lookup_expr="icontains")
    publisher = django_filters.CharFilter(field_name="publisher__name", lookup_expr="icontains")
    shelf = django_filters.CharFilter(field_name="shelf__name", lookup_expr="icontains")

    class Meta:
        model = Book
        fields = {
            "title": ["exact", "icontains"],
            "publication_date": ["exact", "year__gt", "year__lt"],
            "isbn": ["exact", "icontains"],
            "copies": ["exact", "gt", "lt"],
        }
