import django_filters

from .models import User

class UserFilter(django_filters.FilterSet):

    ordering = django_filters.OrderingFilter(
        fields = (
            ('username', 'username'),
            ('email', 'email'),
            ('first_name', 'first_name'),
            ('last_name', 'last_name'),
            ('role', 'role'),
            ('is_active', 'is_active'),
            ('date_joined', 'date_joined'),
        )
    )
    class Meta:
        model = User
        fields = {
            "username": ["exact", "icontains"],
            "email": ["exact", "icontains"],
            "first_name": ["exact", "icontains"],
            "last_name": ["exact", "icontains"],
            "is_active": ["exact"],
            "role": ["exact"],
            "is_staff": ["exact"],
        }