from django.contrib import admin
from .models import Book, User, BorrowRecord

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'published_date', 'number_of_copies_available')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('published_date',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_of_membership', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'date_of_membership')

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date', 'return_date')
    search_fields = ('user__username', 'book__title')
    list_filter = ('borrow_date', 'return_date')
