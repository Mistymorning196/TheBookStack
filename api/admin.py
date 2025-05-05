from django.contrib import admin
from django.utils.html import format_html
from .models import Blog, Group, SiteUser, Reader, Author, Book, Genre, Friendship, Message

#These registers these models to the admin panel

# Friendship Inline
class FriendshipInline(admin.TabularInline):
    """
    Admin Inline for friendship
    """
    model = Friendship
    fk_name = 'user'


# Message Inline
class MessageInline(admin.TabularInline):
    """
    Admin Inline for message
    """
    model = Message
    fk_name = 'user'


#UserBook inline
class UserBookInline(admin.TabularInline):
    """
    Admin Inline for userbook
    """
    model = Reader.user_books.through
    fk_name = 'user'

#ReaderGenre Inline
class ReaderGenreInline(admin.TabularInline):
    """
    Admin Inline for readergenre
    """
    model = Reader.genres.through
    fk_name = 'user'

#bookgenre inline
class BookGenreInline(admin.TabularInline):
    """
    Admin Inline for bookgenre
    """
    model = Book.genres.through
    fk_name = 'book'

#review inline
class ReviewInline(admin.TabularInline):
    """
    Admin Inline for review
    """
    model = Book.reviews.through
    fk_name = 'book'

#comment inline
class CommentInline(admin.TabularInline):
    """
    Admin Inline for comment
    """
    model = Blog.comments.through
    fk_name = 'blog'

#discussion inline
class DiscussionInline(admin.TabularInline):
    """
    Admin Inline for discussion
    """
    model = Group.discussions.through
    fk_name = 'group'


#authorbook inline
class AuthorBookInline(admin.TabularInline):#
    """
    Admin Inline for authorbook
    """
    model = Author.books.through
    fk_name = 'user'

#authorblog inline
class AuthorBlogInline(admin.TabularInline):
    """
    Admin Inline for authorblog
    """
    model = Author.blogs.through
    fk_name = 'user'

#register blog
@admin.register(Blog)
class BookAdmin(admin.ModelAdmin):
    """
    Admin panel for Blog
    """
    inlines = (CommentInline,)

#register group
@admin.register(Group)
class BookAdmin(admin.ModelAdmin):
    """
    Admin panel for Group
    """
    inlines = (DiscussionInline,)

#register book
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin panel for Book
    """
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

#register genre
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Admin panel for Genre
    """
    pass

#register siteuser
@admin.register(SiteUser)
class SiteUserAdmin(admin.ModelAdmin):    
    """
    Admin panel for SiteUser
    """
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_of_birth')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('is_active', 'is_staff')
    ordering = ('username',)

#register reader
@admin.register(Reader)
class ReaderAdmin(SiteUserAdmin):
    """
    Admin panel for Reader model, inheriting from SiteUserAdmin.
    """
    inlines = (FriendshipInline, MessageInline, UserBookInline, ReaderGenreInline,)
    list_display = SiteUserAdmin.list_display + ('book_count',)
    search_fields = SiteUserAdmin.search_fields
    list_filter = SiteUserAdmin.list_filter

#regster author
@admin.register(Author)
class AuthorAdmin(SiteUserAdmin):
    """
    Admin panel for Author model, inheriting from SiteUserAdmin.
    """
    inlines = (AuthorBookInline, AuthorBlogInline,)
    list_display = SiteUserAdmin.list_display
    search_fields = SiteUserAdmin.search_fields
    list_filter = SiteUserAdmin.list_filter
