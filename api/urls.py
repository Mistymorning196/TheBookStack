from django.conf import settings
from django.contrib import admin, auth
from django.urls import include, path
from django.http import HttpResponse

from .views import login_site_user, logout_site_user, signup_site_user, books_api, book_api, site_users_api, site_user_api

# Listing route URLs to views.
urlpatterns = [
    path('', login_site_user, name='site user login'),
    path('login/', login_site_user, name='site user login'),
    path('signup/', signup_site_user, name='site user signup'),
    path('logout/', logout_site_user, name='site user logout'),
    path('books/', books_api, name='books api'),
    path('book/<int:book_id>/', book_api, name='book api'),
    path('site_users/', site_users_api, name='site users api'),
    path('site_user/<int:user_id>/', site_user_api, name='site user api'),
]