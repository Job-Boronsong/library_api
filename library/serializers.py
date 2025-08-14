from rest_framework import serializers
from .models import User, Book, BorrowRecord


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'is_active']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'published_date', 'copies_available']


class BorrowRecordSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    book = serializers.StringRelatedField()

    class Meta:
        model = BorrowRecord
        fields = ['id', 'user', 'book', 'borrowed_at', 'returned_at', 'is_returned']
