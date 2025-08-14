from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User, Book, BorrowRecord
from .serializers import UserSerializer, BookSerializer, BorrowRecordSerializer
from django.utils import timezone


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Only admins can manage users


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def borrow(self, request, pk=None):
        """Borrow a book"""
        book = self.get_object()

        if book.copies_available < 1:
            return Response({"error": "No copies available"}, status=status.HTTP_400_BAD_REQUEST)

        already_borrowed = BorrowRecord.objects.filter(user=request.user, book=book, returned_at__isnull=True).exists()
        if already_borrowed:
            return Response({"error": "You have already borrowed this book"}, status=status.HTTP_400_BAD_REQUEST)

        BorrowRecord.objects.create(user=request.user, book=book)
        book.copies_available -= 1
        book.save()

        return Response({"success": f"You borrowed {book.title}"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def return_book(self, request, pk=None):
        """Return a borrowed book"""
        book = self.get_object()

        try:
            borrow_record = BorrowRecord.objects.get(user=request.user, book=book, returned_at__isnull=True)
        except BorrowRecord.DoesNotExist:
            return Response({"error": "You have not borrowed this book"}, status=status.HTTP_400_BAD_REQUEST)

        borrow_record.returned_at = timezone.now()
        borrow_record.save()

        book.copies_available += 1
        book.save()

        return Response({"success": f"You returned {book.title}"}, status=status.HTTP_200_OK)


class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Users can only see their own borrow records unless they are admin"""
        if self.request.user.is_staff:
            return BorrowRecord.objects.all()
        return BorrowRecord.objects.filter(user=self.request.user)
