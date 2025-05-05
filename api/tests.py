from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from datetime import timedelta
import json
from .models import (
    Genre, Reader, Author, Book, Blog, Group,
    Review, ReaderGenre, AuthorBook, AuthorBlog,
    Comment, Discussion, BookGenre,
    Friendship, Message, UserBook, SiteUser
)




#testing models
class CoreModelTests(TestCase):
    def test_genre_creation(self):
        genre = Genre.objects.create(type="Science Fiction", description="Sci-Fi books")
        self.assertEqual(genre.type, "Science Fiction")


class SiteUserModelTests(TestCase):
    def setUp(self):
        self.reader = Reader.objects.create_user(
            username="reader",
            email="reader@example.com",
            password="readerpass",
            first_name="Read",
            last_name="Er",
            date_of_birth="1992-02-02"
        )
        self.author = Author.objects.create_user(
            username="author",
            email="author@example.com",
            password="authorpass",
            first_name="Write",
            last_name="Er",
            date_of_birth="1985-05-05"
        )

    def test_reader_str(self):
        self.assertEqual(str(self.reader), "Reader: Read Er")

    def test_author_str(self):
        self.assertEqual(str(self.author), "Author: Write Er")


class BookModelTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Book Title",
            author="Book Author",
            blurb="Exciting content",
            isbn="0001112223334"
        )

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Book Title")


class BlogModelTests(TestCase):
    def test_blog_creation(self):
        blog = Blog.objects.create(
            title="Blog Title",
            post="Some interesting thoughts.",
            author="Blog Author"
        )
        self.assertEqual(blog.title, "Blog Title")


class GroupModelTests(TestCase):
    def test_group_creation(self):
        group = Group.objects.create(name="Fiction Fans")
        self.assertEqual(group.name, "Fiction Fans")


class ThroughModelTests(TestCase):
    def setUp(self):
        self.reader1 = Reader.objects.create_user(
            username="reader1",
            email="reader1@example.com",
            password="pass",
            first_name="Alice",
            last_name="R",
            date_of_birth="1991-01-01"
        )
        self.reader2 = Reader.objects.create_user(
            username="reader2",
            email="reader2@example.com",
            password="pass",
            first_name="Bob",
            last_name="R",
            date_of_birth="1992-02-02"
        )
        self.book = Book.objects.create(
            title="Adventure",
            author="Author",
            blurb="Exciting tale",
            isbn="1112223334445"
        )

    def test_friendship(self):
        fs = Friendship.objects.create(
            user=self.reader1,
            friend=self.reader2,
            userUsername="reader1",
            friendUsername="reader2",
            accepted=True
        )
        self.assertTrue(fs.accepted)

    def test_message(self):
        msg = Message.objects.create(
            user=self.reader1,
            friend=self.reader2,
            userUsername="reader1",
            friendUsername="reader2",
            message="Hello!"
        )
        self.assertEqual(msg.message, "Hello!")

    def test_user_book(self):
        ub = UserBook.objects.create(
            user=self.reader1,
            book=self.book,
            status="READING",
            author=self.book.author,
            title=self.book.title
        )
        self.assertEqual(ub.status, "READING")


class RemainingThroughModelTests(TestCase):

    def setUp(self):
        self.genre = Genre.objects.create(type="Fantasy", description="Fantasy books")
        self.reader = Reader.objects.create_user(
            username="reader",
            email="reader@example.com",
            password="testpass123",
            first_name="Alice",
            last_name="Reader",
            date_of_birth="1990-01-01"
        )
        self.author = Author.objects.create_user(
            username="author",
            email="author@example.com",
            password="testpass123",
            first_name="John",
            last_name="Writer",
            date_of_birth="1980-01-01"
        )
        self.book = Book.objects.create(
            title="Mystery Book",
            author="John Writer",
            blurb="Exciting mystery...",
            isbn="1234567890123",
        )
        self.blog = Blog.objects.create(
            title="My Blog",
            post="This is a blog post.",
            author="John Writer"
        )
        self.group = Group.objects.create(name="Readers United")

    def test_review_creation(self):
        review = Review.objects.create(
            user=self.reader,
            book=self.book,
            title="Amazing read",
            username=self.reader.username,
            rating=5,
            message="Loved every bit of it!"
        )
        self.assertEqual(review.rating, 5)

    def test_reader_genre_link(self):
        link = ReaderGenre.objects.create(
            user=self.reader,
            genre=self.genre,
            name=self.genre.type,
            count=3
        )
        self.assertEqual(link.name, "Fantasy")

    def test_author_book_link(self):
        ab = AuthorBook.objects.create(
            user=self.author,
            book=self.book,
            author=self.author.username,
            title=self.book.title
        )
        self.assertEqual(ab.title, "Mystery Book")

    def test_author_blog_link(self):
        ablog = AuthorBlog.objects.create(
            user=self.author,
            blog=self.blog,
            author=self.author.username,
            title=self.blog.title
        )
        self.assertEqual(ablog.title, "My Blog")

    def test_comment_creation(self):
        comment = Comment.objects.create(
            blog=self.blog,
            user=self.reader,
            username=self.reader.username,
            comment="Nice post!"
        )
        self.assertIn("Nice", comment.comment)

    def test_discussion_creation(self):
        discussion = Discussion.objects.create(
            group=self.group,
            user=self.reader,
            username=self.reader.username,
            discussion="What book are we reading next?"
        )
        self.assertIn("book", discussion.discussion)

    def test_book_genre_link(self):
        link = BookGenre.objects.create(
            book=self.book,
            genre=self.genre,
            name=self.genre.type
        )
        self.assertEqual(link.name, "Fantasy")

#testing views 
User = get_user_model()

class AuthViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.reader = Reader.objects.create_user(
            username="readeruser", email="reader@example.com", password="testpass123"
        )
        self.reader.two_factor_token = "123456"
        self.reader.token_generated_at = timezone.now()
        self.reader.save()

        # Update URL references to match actual names from urls.py
        self.login_url = reverse('site user login')
        self.signup_url = reverse('site user signup')
        self.verify_url = reverse('verify_2fa')
        self.logout_url = reverse('site user logout')
        self.update_pass_url = reverse('update password')
        self.update_user_url = reverse('update user')

    def test_login_success_redirects_to_2fa(self):
        response = self.client.post(self.login_url, {
            "username": "readeruser",
            "password": "testpass123"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.verify_url)

    def test_login_failure_renders_form(self):
        response = self.client.post(self.login_url, {
            "username": "wronguser",
            "password": "wrongpass"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")

    def test_verify_2fa_success_redirects(self):
        self.client.login(username="readeruser", password="testpass123")
        response = self.client.post(self.verify_url, {"token": "123456"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("?u=1", response.url)

    def test_verify_2fa_invalid_token(self):
        self.client.login(username="readeruser", password="testpass123")
        response = self.client.post(self.verify_url, {"token": "wrongtoken"})
        self.assertContains(response, "Invalid token")

    def test_verify_2fa_expired_token(self):
        self.reader.token_generated_at = timezone.now() - timedelta(minutes=11)
        self.reader.save()
        self.client.login(username="readeruser", password="testpass123")
        response = self.client.post(self.verify_url, {"token": "123456"})
        self.assertContains(response, "Token expired")

    def test_signup_reader_success(self):
        response = self.client.post(self.signup_url, {
            "first_name": "John",
            "last_name": "Doe",
            "username": "newreader",
            "email": "new@example.com",
            "date_of_birth": "2000-01-01",
            "password": "readerpass",
            "user_type": "reader"
        })
        self.assertEqual(response.status_code, 302)

    def test_logout_redirects_to_login(self):
        self.client.login(username="readeruser", password="testpass123")
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("site user login"), response.url)



class UpdatePasswordTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.reader = Reader.objects.create_user(
            username="readeruser", email="reader@example.com", password="testpass123"
        )
        self.reader.two_factor_token = "123456"
        self.reader.token_generated_at = timezone.now()
        self.reader.save()
        
        # Define the URL for the update password page
        self.update_pass_url = reverse('update password')

    def test_update_password_success(self):
        """ Test that a valid password update redirects after a successful change """
        self.client.login(username="readeruser", password="testpass123")
        response = self.client.post(self.update_pass_url, {
            "password": "newpassword123"
        })
        self.assertEqual(response.status_code, 200)  # Check if it's a redirect


    def test_update_password_failure_empty_password(self):
        """ Test that an empty password raises an error """
        self.client.login(username="readeruser", password="testpass123")
        response = self.client.post(self.update_pass_url, {
            "password": ""  # Empty password
        })
        self.assertEqual(response.status_code, 200)  # Should render the form again
        self.assertContains(response, "This field is required.")  # Check if form error is displayed



class UpdateUsernameTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.reader = Reader.objects.create_user(
            username="readeruser", email="reader@example.com", password="testpass123"
        )
        self.reader.two_factor_token = "123456"
        self.reader.token_generated_at = timezone.now()
        self.reader.save()
        
        self.update_user_url = reverse('update user')

    def test_update_username_success(self):
        """ Test that the username is updated successfully """
        self.client.login(username="readeruser", password="testpass123")
        response = self.client.post(self.update_user_url, {
            "new_username": "newusername"
        })
        self.assertEqual(response.status_code, 200) 


    def test_update_username_failure_taken_username(self):
        """ Test that attempting to take an existing username results in an error """
        another_reader = Reader.objects.create_user(
            username="otheruser", email="other@example.com", password="testpass123"
        )
        self.client.login(username="readeruser", password="testpass123")
        response = self.client.post(self.update_user_url, {
            "new_username": "otheruser"  # The username already exists
        })
        self.assertEqual(response.status_code, 200)  # Should render the form again

    def test_update_username_failure_empty_username(self):
        """ Test that an empty username raises an error """
        self.client.login(username="readeruser", password="testpass123")
        response = self.client.post(self.update_user_url, {
            "new_username": ""  # Empty username
        })
        self.assertEqual(response.status_code, 200)  # Should render the form again


#other views  

#blog tests
class BlogAPITest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_blog(self):
        data = {"title": "Blog Title", "post": "This is a blog post", "author": "Author Name"}
        response = self.client.post("/blogs/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Blog.objects.count(), 1)

    def test_get_blogs(self):
        Blog.objects.create(title="Blog1", post="Post", author="Author")
        response = self.client.get("/blogs/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("blogs", response.json())

    def test_update_blog(self):
        blog = Blog.objects.create(title="Old", post="Old post", author="Someone")
        data = {"title": "New", "post": "Updated post", "author": "Someone"}
        response = self.client.put(f"/blog/{blog.id}/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete_blog(self):
        blog = Blog.objects.create(title="Temp", post="Post", author="Auth")
        response = self.client.delete(f"/blog/{blog.id}/")
        self.assertEqual(response.status_code, 204)

#group tests
class GroupAPITest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_group(self):
        data = {"name": "Readers"}
        response = self.client.post("/groups/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Group.objects.count(), 1)

    def test_get_groups(self):
        Group.objects.create(name="Writers")
        response = self.client.get("/groups/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("groups", response.json())

    def test_update_group(self):
        group = Group.objects.create(name="Old Group")
        data = {"name": "New Group"}
        response = self.client.put(f"/group/{group.id}/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete_group(self):
        group = Group.objects.create(name="ToDelete")
        response = self.client.delete(f"/group/{group.id}/")
        self.assertEqual(response.status_code, 200)

#site user tests
class SiteUserAPITest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_site_user(self):
        data = {
            "first_name": "John", "last_name": "Doe", "email": "john@example.com",
            "date_of_birth": "1990-01-01", "password": "pass1234"
        }
        response = self.client.post("/site_users/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_get_site_users(self):
        SiteUser.objects.create(
            first_name="Jane", last_name="Doe", email="jane@example.com",
            date_of_birth="1990-01-01", password="pass1234"
        )
        response = self.client.get("/site_users/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("site_users", response.json())

    def test_update_site_user(self):
        user = SiteUser.objects.create(first_name="Old", last_name="User", email="old@example.com", date_of_birth="1990-01-01", password="123")
        data = {"first_name": "New", "last_name": "User", "email": "new@example.com", "date_of_birth": "1990-01-01", "password": "newpass"}
        response = self.client.put(f"/site_user/{user.id}/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete_site_user(self):
        user = SiteUser.objects.create(first_name="Delete", last_name="User", email="del@example.com", date_of_birth="1990-01-01", password="123")
        response = self.client.delete(f"/site_user/{user.id}/")
        self.assertEqual(response.status_code, 204)

#reader tests
class ReaderAPITest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_reader(self):
        data = {
            "first_name": "Reader", "last_name": "One", "email": "reader@example.com",
            "date_of_birth": "2000-01-01", "password": "readerpass", "book_count": 5
        }
        response = self.client.post("/readers/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_get_readers(self):
        Reader.objects.create_user(
            username="reader1", email="r1@example.com", password="pass", book_count=0
        )
        response = self.client.get("/readers/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("readers", response.json())
    
    def test_update_reader(self):
        reader = Reader.objects.create_user(username="readerU", email="u@example.com", password="123", book_count=1)
        data = {"email": "updated@example.com", "book_count": 10}
        response = self.client.put(f"/reader/{reader.id}/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete_reader(self):
        reader = Reader.objects.create_user(username="readerD", email="d@example.com", password="123")
        response = self.client.delete(f"/reader/{reader.id}/")
        self.assertEqual(response.status_code, 204)

#author tests
class AuthorAPITest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_author(self):
        data = {
            "first_name": "Auth", "last_name": "Or", "email": "auth@example.com",
            "date_of_birth": "1980-01-01", "password": "authpass", "biography": "Writes stuff"
        }
        response = self.client.post("/authors/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_get_authors(self):
        Author.objects.create(
            first_name="A", last_name="B", email="ab@example.com",
            date_of_birth="1970-01-01", password="pwd", biography="Bio"
        )
        response = self.client.get("/authors/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("authors", response.json())
    
    def test_update_author(self):
        author = Author.objects.create(first_name="Old", last_name="Author", email="old@example.com", date_of_birth="1970-01-01", password="123", biography="Bio")
        data = {"first_name": "New", "last_name": "Author", "email": "new@example.com", "date_of_birth": "1970-01-01", "password": "123", "biography": "Updated Bio"}
        response = self.client.put(f"/author/{author.id}/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete_author(self):
        author = Author.objects.create_user(username="AuthorD",  email="del@example.com", password="123")
        response = self.client.delete(f"/author/{author.id}/")
        self.assertEqual(response.status_code, 204)

#genre tests
class GenreAPITest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_genre(self):
        data = {"type": "Fantasy", "description": "Magic and stuff"}
        response = self.client.post("/genres/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_get_genres(self):
        Genre.objects.create(type="Sci-Fi", description="Space")
        response = self.client.get("/genres/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("genres", response.json())
    
    def test_update_genre(self):
        genre = Genre.objects.create(type="OldType", description="Old Desc")
        data = {"type": "NewType", "description": "New Desc"}
        response = self.client.put(f"/genre/{genre.id}/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete_genre(self):
        genre = Genre.objects.create(type="ToDelete", description="Desc")
        response = self.client.delete(f"/genre/{genre.id}/")
        self.assertEqual(response.status_code, 204)

#friendship tests
class FriendshipAPITest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_friendship(self):
        u1 = Reader.objects.create_user(username="u1", email="u1@example.com", password="pass")
        u2 = Reader.objects.create_user(username="u2", email="u2@example.com", password="pass")
        data = {"user_id": u1.id, "friend_id": u2.id, "accepted": False}
        response = self.client.post("/friendships/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_friendships(self):
        u1 = Reader.objects.create_user(username="f1", email="f1@example.com", password="pass")
        u2 = Reader.objects.create_user(username="f2", email="f2@example.com", password="pass")
        Friendship.objects.create(user=u1, friend=u2, accepted=False)
        response = self.client.get("/friendships/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("friendships", response.json())
    
    def test_update_friendship(self):
        u1 = Reader.objects.create_user(username="fu1", email="fu1@example.com", password="pass")
        u2 = Reader.objects.create_user(username="fu2", email="fu2@example.com", password="pass")
        friendship = Friendship.objects.create(user=u1, friend=u2, accepted=False)
        data = {"user_id": u1.id, "friend_id": u2.id, "accepted": True}
        response = self.client.put(f"/friendship/{friendship.id}/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete_friendship(self):
        u1 = Reader.objects.create_user(username="fd1", email="fd1@example.com", password="pass")
        u2 = Reader.objects.create_user(username="fd2", email="fd2@example.com", password="pass")
        friendship = Friendship.objects.create(user=u1, friend=u2, accepted=False)
        response = self.client.delete(f"/friendship/{friendship.id}/")
        self.assertEqual(response.status_code, 204)


#message tests
class MessageAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Reader.objects.create(username="reader1", email="fd1@example.com", password="pass")
        self.friend = Reader.objects.create(username="reader2", email="fd2@example.com", password="pass")

    def test_create_and_list_messages(self):
        data = {
            "user": self.user.id,
            "friend": self.friend.id,
            "message": "Hi!"
        }
        res = self.client.post("/messages/", json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 200)

        res = self.client.get("/messages/")
        self.assertIn("messages", res.json())

    def test_delete_message(self):
        msg = Message.objects.create(user=self.user, friend=self.friend, message="Hey")
        res = self.client.delete(f"/message/{msg.id}/")
        self.assertEqual(res.status_code, 204)

#user_book tests
class UserBookAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Reader.objects.create(username="reader1", email="fd1@example.com", password="pass")
        self.book = Book.objects.create(title="Mystery Book", author="John Writer", blurb="Exciting mystery...", isbn="1234567890123",)
        self.client.force_login(self.user)

    def test_create_and_list_user_books(self):
        data = {
            "user_id": self.user.id,
            "book_id": self.book.id,
            "status": "reading"
        }
        res = self.client.post("/user_books/", json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 200)

        res = self.client.get("/user_books/")
        self.assertIn("user_books", res.json())

    def test_update_and_delete_user_book(self):
        user_book = UserBook.objects.create(user=self.user, book=self.book, status="completed")

        update_data = {"status": "dropped"}
        res = self.client.put(f"/user_book/{user_book.id}/", json.dumps(update_data), content_type="application/json")
        self.assertEqual(res.status_code, 200)

        res = self.client.delete(f"/user_book/{user_book.id}/")
        self.assertEqual(res.status_code, 204)

#author_book tests
class AuthorBookAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Author.objects.create(username="author1", email="fd1@example.com", password="pass")
        self.book = Book.objects.create(title="Mystery Book", author="John Writer", blurb="Exciting mystery...", isbn="1234567890123",)
        self.client.force_login(self.user)

    def test_create_and_list_author_books(self):
        data = {"user_id": self.user.id, "book_id": self.book.id}
        res = self.client.post("/author_books/", json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 200)

        res = self.client.get("/author_books/")
        self.assertIn("author_books", res.json())

    def test_delete_author_book(self):
        ab = AuthorBook.objects.create(user=self.user, book=self.book)
        res = self.client.delete(f"/author_book/{ab.id}/")
        self.assertEqual(res.status_code, 204)

#author_blog tests
class AuthorBlogAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Author.objects.create(username="author1", email="fd1@example.com", password="pass")
        self.blog = Blog.objects.create(title="Temp", post="Post", author="Auth")
        self.client.force_login(self.user)

    def test_create_and_list_author_blogs(self):
        data = {"user_id": self.user.id, "blog_id": self.blog.id}
        res = self.client.post("/author_blogs/", json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 200)

        res = self.client.get("/author_blogs/")
        self.assertIn("author_blogs", res.json())

    def test_delete_author_blog(self):
        ab = AuthorBlog.objects.create(user=self.user, blog=self.blog)
        res = self.client.delete(f"/author_blog/{ab.id}/")
        self.assertEqual(res.status_code, 204)

#reader_genre tests
class ReaderGenreAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Reader.objects.create(username="reader1", email="fd1@example.com", password="pass")
        self.genre = Genre.objects.create(type="Fiction", description="fake")
        self.client.force_login(self.user)

    def test_create_and_list_reader_genres(self):
        data = {"user_id": self.user.id, "genre_id": self.genre.id}
        res = self.client.post("/reader_genres/", json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 200)

        res = self.client.get("/reader_genres/")
        self.assertIn("reader_genre", res.json())

    def test_update_and_delete_reader_genre(self):
        rg = ReaderGenre.objects.create(user=self.user, genre=self.genre, count=2)
        res = self.client.put(f"/reader_genre/{rg.id}/", json.dumps({"count": 5}), content_type="application/json")
        self.assertEqual(res.status_code, 200)

        res = self.client.delete(f"/reader_genre/{rg.id}/")
        self.assertEqual(res.status_code, 204)

#book_genre tests
class BookGenreAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.book = Book.objects.create(title="Mystery Book", author="John Writer", blurb="Exciting mystery...", isbn="1234567890123",)
        self.genre = Genre.objects.create(type="Fantasy", description="Magic")

    def test_create_and_list_book_genres(self):
        data = {"book_id": self.book.id, "genre_id": self.genre.id}
        res = self.client.post("/book_genres/", json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 200)

        res = self.client.get("/book_genres/")
        self.assertIn("book_genre", res.json())

    def test_delete_book_genre(self):
        bg = BookGenre.objects.create(book=self.book, genre=self.genre)
        res = self.client.delete(f"/book_genre/{bg.id}/")
        self.assertEqual(res.status_code, 204)

#review tests
class ReviewAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Reader.objects.create(username="reader1", email="fd1@example.com", password="pass")
        self.book = Book.objects.create(title="Mystery Book", author="John Writer", blurb="Exciting mystery...", isbn="1234567890123",)
        self.client.force_login(self.user)

    def test_create_and_list_reviews(self):
        data = {
            "user_id": self.user.id,
            "book_id": self.book.id,
            "title": "Great!",
            "rating": 5,
            "message": "Loved it!"
        }
        res = self.client.post("/reviews/", json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 200)

        res = self.client.get("/reviews/")
        self.assertIn("reviews", res.json())

    def test_update_and_delete_review(self):
        rev = Review.objects.create(user=self.user, book=self.book, title="Old", rating=3, message="ok")
        res = self.client.put(f"/review/{rev.id}/", json.dumps({
            "title": "New", "rating": 4, "message": "Better"
        }), content_type="application/json")
        self.assertEqual(res.status_code, 200)

        res = self.client.delete(f"/review/{rev.id}/")
        self.assertEqual(res.status_code, 204)

#comment tests
class CommentAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Reader.objects.create(username="reader1", email="fd1@example.com", password="pass")
        self.blog = Blog.objects.create(title="Temp", post="Post", author="Auth")
        self.client.force_login(self.user)

    def test_create_and_list_comments(self):
        data = {
            "user_id": self.user.id,
            "blog_id": self.blog.id,
            "comment": "Nice read!"
        }
        res = self.client.post("/comments/", json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 200)

        res = self.client.get("/comments/")
        self.assertIn("comments", res.json())

    def test_delete_comment(self):
        c = Comment.objects.create(user=self.user, blog=self.blog, comment="Ok")
        res = self.client.delete(f"/comment/{c.id}/")
        self.assertEqual(res.status_code, 204)

#discussion tests
class DiscussionAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Reader.objects.create(username="reader1", email="fd1@example.com", password="pass")
        self.group = Group.objects.create(name="Group 1")
        self.client.force_login(self.user)

    def test_create_and_list_discussions(self):
        data = {
            "user_id": self.user.id,
            "group_id": self.group.id,
            "discussion": "Let's talk books!"
        }
        res = self.client.post("/discussions/", json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 200)

        res = self.client.get("/discussions/")
        self.assertIn("discussions", res.json())

    def test_delete_discussion(self):
        d = Discussion.objects.create(user=self.user, group=self.group, discussion="Discussion content")
        res = self.client.delete(f"/discussion/{d.id}/")
        self.assertEqual(res.status_code, 204)

    

#book tests
class BooksAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.book_1 = Book.objects.create(
            title="Book 1",
            author="Author 1",
            blurb="A great book",
            isbn="1234567890"
        )
        self.book_2 = Book.objects.create(
            title="Book 2",
            author="Author 2",
            blurb="Another great book",
            isbn="0987654321"
        )


    def test_create_book(self):
        data = {
            "title": "New Book",
            "author": "New Author",
            "blurb": "A thrilling story",
            "isbn": "1122334455",
        }
        res = self.client.post("/books/", data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()["title"], "New Book")

      

    def test_get_books(self):
        res = self.client.get("/books/")
        self.assertEqual(res.status_code, 200)
        books = res.json()['books']
        self.assertEqual(len(books), 2)  # 2 books created in setUp

    def test_search_books(self):
        res = self.client.get("/books/?search=Book 1")
        self.assertEqual(res.status_code, 200)
        books = res.json()['books']
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]['title'], "Book 1")

class BookAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.book = Book.objects.create(
            title="Book 1",
            author="Author 1",
            blurb="A great book",
            isbn="1234567890"
        )

    def test_get_single_book(self):
        res = self.client.get(f"/book/{self.book.id}/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['title'], "Book 1")

    def test_update_book_with_json(self):
        data = {
            "title": "Updated Book Title",
            "author": "Updated Author",
            "blurb": "Updated blurb",
            "isbn": "1122334455"
        }
        res = self.client.put(f"/book/{self.book.id}/", json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['title'], "Updated Book Title")
        self.assertEqual(res.json()['author'], "Updated Author")

    def test_delete_book(self):
        res = self.client.delete(f"/book/{self.book.id}/")
        self.assertEqual(res.status_code, 204)
        # Confirm the book is deleted
        res = self.client.get(f"/book/{self.book.id}/")
        self.assertEqual(res.status_code, 404)











