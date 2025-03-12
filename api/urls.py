from django.conf import settings
from django.contrib import admin, auth
from django.urls import include, path
from django.http import HttpResponse

from .views import friendship_api, friendships_api, genre_api, genres_api, login_site_user, logout_site_user, message_api, messages_api, review_api, reviews_api, signup_site_user, books_api, book_api, site_users_api, site_user_api, user_book_api, user_books_api

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
    path('genres/', genres_api, name='genres api'),
    path('genre/<int:genre_id>/', genre_api, name='genre api'),
    path('friendships/', friendships_api, name='friendships api'),
    path('friendship/<int:friendship_id>/', friendship_api, name='friendship api'),
     path('messages/', messages_api, name='messages api'),
    path('message/<int:message_id>/', message_api, name='message api'),
    path('user_books/', user_books_api, name='user books api'),
    path('user_book/<int:user_book_id>/', user_book_api, name='user book api'),
    path('reviews/', reviews_api, name='reviews api'),
    path('review/<int:review_id>/', review_api, name='review api'),
]