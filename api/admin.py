from django.contrib import admin
from .models import Book, SiteUser, Genre




'''Register the friendship through model to the admin panel'''

class FriendshipInline(admin.TabularInline):
    model = SiteUser.friends.through
    fk_name = 'user'

'''Register the UserBook through model to the admin panel'''

class UserBookInline(admin.TabularInline):
    model = SiteUser.user_books.through
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
    inlines = (FriendshipInline, UserBookInline,)
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_of_birth')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('is_active', 'is_staff')
    ordering = ('username',)
