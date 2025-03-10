import django_filters

from .models import Book, Shelf, Loan, FinePayment, Publisher, Author

class ShelfFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(
        fields = (
            ('name', 'name'),
        )
    )

    class Meta:
        model = Shelf
        fields = {
            "name": ["exact", "icontains"],
        }

class AuthorFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(
        fields = (
            ('name', 'name'),
        )
    )

    class Meta:
        model = Author
        fields = {
            "name": ["exact", "icontains"]
        }

class PublisherFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(
        fields = (
            ('name', 'name'),
            ('email', 'email'),
        )
    )
    
    class Meta:
        model = Publisher
        fields = {
            "name": ["exact", "icontains"],
            "email": ["exact", "icontains"],
        }

class BookFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(
        fields = (
            ('title', 'title'),
            ('author__name', 'author'),
            ('publisher__name', 'publisher'),
            ('publication_date', 'publication_date'),
            ('copies', 'copies'),
            ('shelf__name', 'shelf'),
        )
    )

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

class LoanFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(
        fields = (
            ('loan_date', 'loan_date'),
            ('due_date', 'due_date'),
            ('return_date', 'return_date'),
            ('fine_amount', 'fine_amount'),
            ('is_paid', 'is_paid'),
        )
    )
    
    book = django_filters.CharFilter(field_name="book__title", lookup_expr="icontains")
    user = django_filters.CharFilter(field_name="user__username", lookup_expr="icontains")

    class Meta:
        model = Loan
        fields = {
            "loan_date": ["exact", "gt", "lt"],
            "due_date": ["exact", "gt", "lt"],
            "return_date": ["exact", "gt", "lt"],
            "status": ["exact"],
            "fine_amount": ["exact", "gt", "lt"],
            "is_paid": ["exact"],
        }
