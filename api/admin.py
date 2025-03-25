from django.contrib import admin
from .models import SiteUser, Reader, Author, Book, Genre, Friendship, Message, UserBook, Review

# Friendship Inline
class FriendshipInline(admin.TabularInline):
    model = Friendship
    fk_name = 'user'


# Message Inline
class MessageInline(admin.TabularInline):
    model = Message
    fk_name = 'user'


'''Register the UserBook through model to the admin panel'''

class UserBookInline(admin.TabularInline):
    model = Reader.user_books.through
    fk_name = 'user'

'''Register the friendship through model to the admin panel'''

class ReviewInline(admin.TabularInline):
    model = Book.reviews.through
    fk_name = 'book'

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = (ReviewInline,)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


'''Register the user model to the admin panel'''
@admin.register(SiteUser)
class SiteUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_of_birth')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('is_active', 'is_staff')
    ordering = ('username',)

@admin.register(Reader)
class ReaderAdmin(SiteUserAdmin):
    """
    Admin panel for Reader model, inheriting from SiteUserAdmin.
    """
    inlines = (FriendshipInline, MessageInline, UserBookInline,)
    list_display = SiteUserAdmin.list_display + ('book_count',)
    search_fields = SiteUserAdmin.search_fields
    list_filter = SiteUserAdmin.list_filter

@admin.register(Author)
class AuthorAdmin(SiteUserAdmin):
    """
    Admin panel for Author model, inheriting from SiteUserAdmin.
    """
    list_display = SiteUserAdmin.list_display
    search_fields = SiteUserAdmin.search_fields
    list_filter = SiteUserAdmin.list_filter
