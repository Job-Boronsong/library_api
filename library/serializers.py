from rest_framework import serializers
from .models import User, Book, BorrowRecord
from django.contrib.auth.hashers import make_password


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

    def validate_isbn(self, value):
        """Ensure ISBN is unique and exactly 13 characters."""
        if len(value) != 13:
            raise serializers.ValidationError("ISBN must be exactly 13 characters long.")
        # Check uniqueness at the serializer level for cleaner error
        if Book.objects.filter(isbn=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("A book with this ISBN already exists.")
        return value


class BorrowRecordSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = BorrowRecord
        fields = ['id', 'user', 'book', 'book_title', 'borrowed_at', 'returned_at', 'is_returned']
        read_only_fields = ['borrowed_at', 'returned_at', 'is_returned']

    def validate(self, attrs):
        """Ensure user is not borrowing the same book twice without returning it."""
        user = attrs.get('user')
        book = attrs.get('book')
        if self.instance is None:  # Only check on create
            if BorrowRecord.objects.filter(user=user, book=book, returned_at__isnull=True).exists():
                raise serializers.ValidationError("You already have this book borrowed and not returned.")
            if book.copies_available < 1:
                raise serializers.ValidationError("No copies of this book are currently available.")
        return attrs
