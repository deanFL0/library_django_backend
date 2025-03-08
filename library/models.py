from django.db import models
from django.utils import timezone

from user.models import User

class Shelf(models.Model):
    shelf_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

class Publisher(models.Model):
    publisher_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()

class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)

class Book(models.Model):
    def unknown_author():
        author, _ = Author.objects.get_or_create(name="Unknown")
        return author.author_id
    
    def unknown_publisher():
        publisher, _ = Publisher.objects.get_or_create(name="Unknown", address="Unknown", phone="Unknown", email="Unknown")
        return publisher.publisher_id

    book_id = models.AutoField(primary_key=True)
    book_img = models.ImageField(upload_to='media/book_images/')
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.SET(unknown_author), related_name="books")
    publisher = models.ForeignKey(Publisher, on_delete=models.SET(unknown_publisher), related_name="books")
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13)
    copies = models.IntegerField()
    shelf = models.ForeignKey(Shelf, on_delete=models.SET_NULL, null=True, related_name="books")

    @property
    def available_copies(self):
        borrowed_count = self.loans.filter(return_date__isnull=True).count()
        return self.copies - borrowed_count

class Loan(models.Model):
    class LoanStatus(models.TextChoices):
        BORROWED = "borrowed", "Borrowed"
        RETURNED = "returned", "Returned"

    loan_id = models.AutoField(primary_key=True)
    loan_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=LoanStatus.choices, default=LoanStatus.BORROWED)
    fine_amount = models.FloatField()
    is_paid = models.BooleanField(default=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="loans")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_overdue(self):
        if self.return_date:
            return self.return_date > self.due_date
        return False
    
    def calculate_fine(self):
        daily_rate = 0.25

        # Check if book is overdue and calculate fine
        if self.return_date and self.due_date and self.return_date > self.due_date:
            overdue_days = (self.return_date - self.due_date).days
            return round(overdue_days * daily_rate, 2)
        else:
            return 0.00
        
    def update_payment_status(self):
        total_paid = self.fine_payments.aggregate(models.Sum("amount_paid"))["amount_paid__sum"]
        self.is_paid = total_paid >= self.fine_amount
        self.save(update_fields=["is_paid"])


    def save(self, *args, **kwargs):
        """Override save method to check fine before saving."""

        # Automatically set return date if status is returned
        if self.status == self.LoanStatus.RETURNED and not self.return_date:
            self.return_date = timezone.localdate()

        self.fine_amount = self.calculate_fine()
        super().save(*args, **kwargs)

class FinePayment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    payment_date = models.DateField(auto_now_add=True)
    amount_paid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fine_payments")
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="fine_payments")

    def save(self, *args, **kwargs):
        """Override save method to update loan status."""
        super().save(*args, **kwargs)
        self.loan.update_payment_status()