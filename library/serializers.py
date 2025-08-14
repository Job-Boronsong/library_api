from rest_framework import serializers
from .models import Book, Loan, User  # Ensure these models exist in models.py

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'available']

class LoanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = Loan
        fields = ['id', 'user', 'book', 'loan_date', 'return_date', 'returned']
