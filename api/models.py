from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# Genre Model
class Genre(models.Model):
    type = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.type}"
    
    def as_dict(self):
        return {  
            'id': self.id,  
            'type': self.type,
            'description': self.description,
        }

# SiteUser Model (must be defined before Book, Friendship, UserBook, Review)
class SiteUser(AbstractUser):
    """
    Class for the model user extending abstract user 
    """ 
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(default='2000-01-01')
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def as_dict(self):
        return {  
            'id': self.id,  
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'date_of_birth': self.date_of_birth,
            'password': self.password,
 
        }

class Reader(SiteUser):
    """
    Reader model extending SiteUser with additional attributes.
    """
    book_count = models.IntegerField(default=0)
    messages = models.ManyToManyField("self", through="Message", symmetrical=False, related_name="messages_with+")
    user_books = models.ManyToManyField("Book", through="UserBook")
    friends = models.ManyToManyField("self", through="Friendship", symmetrical=False, related_name="friends_with+")
    genres = models.ManyToManyField(Genre, through="ReaderGenre")

    class Meta:
        verbose_name = "Reader"
        verbose_name_plural = "Readers"

    def __str__(self):
        return f"Reader: {self.first_name} {self.last_name}"

    def as_dict(self):
        data = super().as_dict()  # Get the parent class dictionary
        data.update({
            'book_count': self.book_count,
        })
        return data

class Author(SiteUser):
    """
    Author model extending SiteUser with additional attributes.
    """
    biography = models.TextField(blank=True, null=True)  # Example attribute

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return f"Author: {self.first_name} {self.last_name}"

    def as_dict(self):
        data = super().as_dict()  # Get the parent class dictionary
        data.update({
            'biography': self.biography,
        })
        return data   


# Book Model
class Book(models.Model):
    """
    Class for the model Book
    """ 
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    blurb = models.TextField(max_length=2000)
    isbn = models.CharField(max_length=100)
    #placeholder for image file for cover picture
    genres = models.ManyToManyField(Genre, through="BookGenre")
    reviews = models.ManyToManyField(Reader, through="Review")  # Proper Many-to-Many with Review

    def as_dict(self):
        return {
            'id': self.id,
            'api': reverse('book api', args=[self.id]),
            'title': self.title,
            'author': self.author,
            'blurb': self.blurb,
            'isbn': self.isbn,
        }
    
# Book Model
class Blog(models.Model):
    """
    Class for the model Book
    """ 
    title = models.CharField(max_length=100)
    post = models.TextField(max_length=2000)
    comments = models.ManyToManyField(Reader, through="Comment")  # Proper Many-to-Many with Review

    def as_dict(self):
        return {
            'id': self.id,
            'api': reverse('blog api', args=[self.id]),
            'title': self.title,
            'post': self.post,
        }
    
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(Reader, on_delete=models.CASCADE)
    comment = models.TextField(max_length=2000)

    def as_dict(self):
        return {
            'id': self.id,
            'api': reverse('reader genre api', args=[self.id]),
            'blog': self.blog.id,
            'user': self.user.id,
            'comment': self.comment,
        }
    
#ReaderGenre Model
class ReaderGenre(models.Model):  
    """
    This class is the ReaderGenres Model which is a through model 
    which creates a many-to-many relationship between users and books.
    """
    user = models.ForeignKey(Reader, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default=None)

    def as_dict(self):
        return {
            'id': self.id,
            'api': reverse('reader genre api', args=[self.id]),
            'user': self.user.id,
            'genre': self.genre.id,
            'name': self.genre.type,
        }

# ReaderGenre Model
class BookGenre(models.Model):  
    """
    This class is the ReaderGenres Model which is a through model 
    which creates a many-to-many relationship between users and books.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default=None)

    def as_dict(self):
        return {
            'id': self.id,
            'api': reverse('book genre api', args=[self.id]),
            'book': self.book.id,
            'genre': self.genre.id,
            'name': self.genre.type,
        }

# Friendship Model
class Friendship(models.Model):
    """
    This class is the Friendship Model which is a through model 
    which creates a many-to-many relationship between site user and friend.
    """
    user = models.ForeignKey(Reader, related_name="from_user", on_delete=models.CASCADE)
    friend = models.ForeignKey(Reader, related_name="to_user", on_delete=models.CASCADE)
    userUsername = models.CharField(max_length=100, default="username")
    friendUsername = models.CharField(max_length=100, default="username")
    accepted = models.BooleanField(default=False)

    def as_dict(self):
        return {
            'id': self.id,
            'api': reverse('friendship api', args=[self.id]),
            'user': self.user.id,
            'friend': self.friend.id,
            'userUsername': self.user.username,
            'friendUsername': self.friend.username,
            'accepted': self.accepted,
        }
    
class Message(models.Model):
    """
    This class is the Message Model which is a through model 
    which creates a many-to-many relationship between site user and friend.
    """
    user = models.ForeignKey(Reader, related_name="messages_from", on_delete=models.CASCADE)
    friend = models.ForeignKey(Reader, related_name="messages_to", on_delete=models.CASCADE)
    userUsername = models.CharField(max_length=100, default="username")
    friendUsername = models.CharField(max_length=100, default="username")
    message = models.TextField(max_length=1000)

    def as_dict(self):
        return {
            'id': self.id,
            'api': reverse('friendship api', args=[self.id]),
            'user': self.user.id,
            'friend': self.friend.id,
            'userUsername': self.user.username,
            'friendUsername': self.friend.username,
            'message': self.message,
        }

# UserBook Model
class UserBook(models.Model): 
    """
    This class is the UserBooks Model which is a through model 
    which creates a many-to-many relationship between users and books.
    """
    STATUS_CHOICES = [
        ("COMPLETED", 'Completed'),
        ("READING", 'Reading'),
        ("WISHLIST", 'Wishlist'),
    ]

    user = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="START")

    def as_dict(self):
        return {
            'id': self.id,
            'api': reverse('user book api', args=[self.id]),
            'user': self.user.id,
            'book': self.book.id,
            'status': self.status,
        }

# Review Model
class Review(models.Model):  # Corrected from models.model to models.Model
    """
    This class is the Review Model which is a through model 
    which creates a many-to-many relationship between users and books.
    """
    RATING_CHOICES = [
        (0, '0 Stars'),
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    user = models.ForeignKey(Reader, on_delete=models.CASCADE)  # Added on_delete to prevent migration errors
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Foreign key for book reference
    title = models.CharField(max_length=100, default='Title')
    username = models.CharField(max_length=100, default='username')
    rating = models.IntegerField(default=0, choices=RATING_CHOICES)
    message = models.TextField(max_length=2000)

    def as_dict(self):
        return {
            'id': self.id,
            'api': reverse('review api', args=[self.id]),
            'user': self.user.id,
            'book': self.book.id,
            'title': self.title,
            'username': self.user.username,
            'rating': self.rating,
            'message': self.message,
        }
