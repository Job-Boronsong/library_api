from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import Book, User, BorrowRecord
from .serializers import BookSerializer, UserSerializer, BorrowRecordSerializer
from .permissions import IsAdminOrReadOnly, IsAdmin, IsOwnerOrAdmin


# ---------------------------
# User ViewSet
# ---------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'create', 'destroy']:
            permission_classes = [IsAdmin]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [perm() for perm in permission_classes]


# ---------------------------
# Book ViewSet
# ---------------------------
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['author', 'isbn']
    search_fields = ['title', 'author', 'isbn']

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def borrow(self, request, pk=None):
        book = self.get_object()
        user = request.user

        # Check availability
        if book.copies_available <= 0:
            return Response({"error": "No copies available"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already borrowed this book
        if BorrowRecord.objects.filter(user=user, book=book, returned_at__isnull=True).exists():
            return Response({"error": "You already borrowed this book"}, status=status.HTTP_400_BAD_REQUEST)

        # Borrow book
        BorrowRecord.objects.create(user=user, book=book, borrowed_at=timezone.now())
        book.copies_available -= 1
        book.save()
        return Response({"message": f"You borrowed '{book.title}'"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def return_book(self, request, pk=None):
        book = self.get_object()
        user = request.user

        record = BorrowRecord.objects.filter(user=user, book=book, returned_at__isnull=True).first()
        if not record:
            return Response({"error": "You have not borrowed this book"}, status=status.HTTP_400_BAD_REQUEST)

        # Return book
        record.returned_at = timezone.now()
        record.save()
        book.copies_available += 1
        book.save()
        return Response({"message": f"You returned '{book.title}'"}, status=status.HTTP_200_OK)


# ---------------------------
# BorrowRecord ViewSet
# ---------------------------
class BorrowRecordViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BorrowRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Admins can see all records
        if user.is_staff:
            return BorrowRecord.objects.all()
        # Members only see their own history
        return BorrowRecord.objects.filter(user=user)
