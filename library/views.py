from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User, Book, BorrowRecord
from .serializers import UserSerializer, BookSerializer, BorrowRecordSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update', 'partial_update', 'list']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def available(self, request):
        books = Book.objects.filter(copies_available__gt=0)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)


class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own borrow records unless admin
        if self.request.user.is_staff:
            return BorrowRecord.objects.all()
        return BorrowRecord.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def borrow_book(self, request):
        book_id = request.data.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        if book.copies_available < 1:
            return Response({"error": "No copies available"}, status=status.HTTP_400_BAD_REQUEST)

        if BorrowRecord.objects.filter(user=request.user, book=book, returned_at__isnull=True).exists():
            return Response({"error": "You have already borrowed this book"}, status=status.HTTP_400_BAD_REQUEST)

        BorrowRecord.objects.create(user=request.user, book=book)
        book.copies_available -= 1
        book.save()

        return Response({"success": f"You have borrowed '{book.title}'"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def return_book(self, request):
        record_id = request.data.get('record_id')
        try:
            record = BorrowRecord.objects.get(id=record_id, user=request.user, returned_at__isnull=True)
        except BorrowRecord.DoesNotExist:
            return Response({"error": "No such borrow record found"}, status=status.HTTP_404_NOT_FOUND)

        record.returned_at = timezone.now()
        record.save()

        book = record.book
        book.copies_available += 1
        book.save()

        return Response({"success": f"You have returned '{book.title}'"}, status=status.HTTP_200_OK)
