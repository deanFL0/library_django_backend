from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import Book, Loan, Shelf

@receiver([post_save, post_delete], sender=Book)
def invalidate_book_cache(sender, instance, **kwargs):
    """Invalidate book cache on save or delete."""
    print("Invalidating cache")
    cache.delete_pattern("*book_list*")

@receiver([post_save, post_delete], sender=Loan)
def invalidate_loan_cache(sender, instance, **kwargs):
    """Invalidate loan cache on save or delete."""
    print("Invalidating cache")
    cache.delete_pattern("*loan_list*")

@receiver([post_save, post_delete], sender=Shelf)
def invalidate_shelf_cache(sender, instance, **kwargs):
    """Invalidate shelf cache on save or delete."""
    print("Invalidating cache")
    cache.delete_pattern("*shelf_list*")