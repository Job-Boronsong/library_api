from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings

# Custom User model
class User(AbstractUser):
    # We can extend this later if needed
    date_of_membership = models.DateField(auto_now_add=True)
    active_status = models.BooleanField(default=True)

    def __str__(self):
        return self.username


# Book model
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField(default=timezone.now)
    number_of_copies_available = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def available(self):
        return self.number_of_copies_available > 0


# Loan / Borrow record
class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"

class BorrowRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} borrowed {self.book}"