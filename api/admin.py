from django.contrib import admin
from django.utils.html import format_html
from .models import Blog, Group, SiteUser, Reader, Author, Book, Genre, Friendship, Message

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

'''Register the ReaderGenre through model to the admin panel'''

class ReaderGenreInline(admin.TabularInline):
    model = Reader.genres.through
    fk_name = 'user'

'''Register the BookGenre through model to the admin panel'''

class BookGenreInline(admin.TabularInline):
    model = Book.genres.through
    fk_name = 'book'

'''Register the review through model to the admin panel'''

class ReviewInline(admin.TabularInline):
    model = Book.reviews.through
    fk_name = 'book'


'''Register the comment through model to the admin panel'''

class CommentInline(admin.TabularInline):
    model = Blog.comments.through
    fk_name = 'blog'

'''Register the comment through model to the admin panel'''

class DiscussionInline(admin.TabularInline):
    model = Group.discussions.through
    fk_name = 'group'

'''Register the author book through model to the admin panel'''

class AuthorBookInline(admin.TabularInline):
    model = Author.books.through
    fk_name = 'user'

'''Register the author book through model to the admin panel'''

class AuthorBlogInline(admin.TabularInline):
    model = Author.blogs.through
    fk_name = 'user'

@admin.register(Blog)
class BookAdmin(admin.ModelAdmin):
    inlines = (CommentInline,)

@admin.register(Group)
class BookAdmin(admin.ModelAdmin):
    inlines = (DiscussionInline,)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = (ReviewInline, BookGenreInline,)
    list_display = ('title', 'author', 'isbn', 'cover_preview')
    readonly_fields = ('cover_preview',)
    fields = (
        'title',
        'author',
        'blurb',
        'isbn',
        'cover_image',
        'cover_preview',
    )

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="100" style="border-radius: 4px;" />', obj.cover_image.url)
        return "(No cover image)"
    cover_preview.short_description = 'Cover Preview'

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
    inlines = (FriendshipInline, MessageInline, UserBookInline, ReaderGenreInline,)
    list_display = SiteUserAdmin.list_display + ('book_count',)
    search_fields = SiteUserAdmin.search_fields
    list_filter = SiteUserAdmin.list_filter

@admin.register(Author)
class AuthorAdmin(SiteUserAdmin):
    """
    Admin panel for Author model, inheriting from SiteUserAdmin.
    """
    inlines = (AuthorBookInline, AuthorBlogInline,)
    list_display = SiteUserAdmin.list_display
    search_fields = SiteUserAdmin.search_fields
    list_filter = SiteUserAdmin.list_filter
