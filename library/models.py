from django.db import models

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
        OVERDUE = "overdue", "Overdue"

    loan_id = models.AutoField(primary_key=True)
    loan_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField()
    status = models.CharField(max_length=10, choices=LoanStatus.choices, default=LoanStatus.BORROWED)
    fine_amount = models.IntegerField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="loans")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_overdue(self):
        return self.return_date > self.due_date
    
    def calculate_fine(self):
        daily_rate = 0.15

        if self.is_overdue():
            overdue_days = (self.return_date - self.due_date).days
            self.fine_amount = round(overdue_days * daily_rate, 2)
        else:
            self.fine_amount = 0

        self.save(update_fields=['fine_amount'])

    def save(self, *args, **kwargs):
        """Override save method to check fine before saving."""
        self.calculate_fine()
        super().save(*args, **kwargs)

class FinePayment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    payment_date = models.DateField()
    amount_paid = models.IntegerField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fine_payments")
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="fine_payments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)