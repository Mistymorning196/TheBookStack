from django.contrib import admin
from .models import Book, SiteUser 

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


'''Register the user model to the admin panel'''
@admin.register(SiteUser)
class SiteUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_of_birth')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('is_active', 'is_staff')
    ordering = ('username',)
