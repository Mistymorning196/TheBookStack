from django.conf import settings
from django.contrib import admin, auth
from django.urls import include, path
from django.http import HttpResponse

from .views import author_api, author_blog_api, author_blogs_api, author_book_api, author_books_api, authors_api, blog_api, blogs_api, book_genre_api, book_genres_api, comment_api, comments_api, friendship_api, friendships_api, genre_api, genres_api, login_site_user, logout_site_user, message_api, messages_api, reader_api, reader_genre_api, reader_genres_api, readers_api, review_api, reviews_api, signup_site_user, books_api, book_api, site_users_api, site_user_api, update_password, update_username, user_book_api, user_books_api

# Listing route URLs to views.
urlpatterns = [
    path('', login_site_user, name='site user login'),
    path('login/', login_site_user, name='site user login'),
    path('signup/', signup_site_user, name='site user signup'),
    path('logout/', logout_site_user, name='site user logout'),
    path('updatePass/', update_password, name='update password'),
    path('updateUser/', update_username, name='update user'),
    path('books/', books_api, name='books api'),
    path('book/<int:book_id>/', book_api, name='book api'),
    path('site_users/', site_users_api, name='site users api'),
    path('site_user/<int:user_id>/', site_user_api, name='site user api'),
    path('readers/', readers_api, name='readers api'),
    path('reader/<int:reader_id>/', reader_api, name='reader api'),
    path('authors/', authors_api, name='authors api'),
    path('author/<int:author_id>/', author_api, name='author api'),
    path('genres/', genres_api, name='genres api'),
    path('genre/<int:genre_id>/', genre_api, name='genre api'),
    path('blogs/', blogs_api, name='blogs api'),
    path('blog/<int:blog_id>/', blog_api, name='blog api'),
    path('friendships/', friendships_api, name='friendships api'),
    path('friendship/<int:friendship_id>/', friendship_api, name='friendship api'),
    path('messages/', messages_api, name='messages api'),
    path('message/<int:message_id>/', message_api, name='message api'),
    path('user_books/', user_books_api, name='user books api'),
    path('user_book/<int:user_book_id>/', user_book_api, name='user book api'),
    path('author_books/', author_books_api, name='author books api'),
    path('author_book/<int:author_book_id>/', author_book_api, name='author book api'),
    path('author_blogs/', author_blogs_api, name='author blogs api'),
    path('author_blog/<int:author_blog_id>/', author_blog_api, name='author blog api'),
    path('reader_genres/', reader_genres_api, name='reader genres api'),
    path('reader_genre/<int:reader_genre_id>/', reader_genre_api, name='reader genre api'),
    path('book_genres/', book_genres_api, name='book genres api'),
    path('book_genre/<int:book_genre_id>/', book_genre_api, name='book genre api'),
    path('reviews/', reviews_api, name='reviews api'),
    path('review/<int:review_id>/', review_api, name='review api'),
    path('comments/', comments_api, name='comments api'),
    path('comment/<int:comment_id>/', comment_api, name='comment api'),
]