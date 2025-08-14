from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Book, BorrowRecord


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'date_of_membership', 'is_active', 'is_staff']
        read_only_fields = ['date_of_membership']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BorrowRecordSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = BorrowRecord
        fields = ['id', 'user', 'book', 'book_title', 'borrowed_at', 'returned_at', 'is_returned']
        read_only_fields = ['borrowed_at', 'returned_at', 'is_returned']
