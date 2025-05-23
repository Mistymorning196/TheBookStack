import json
from django.conf import settings
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q
from django.contrib.auth import get_user_model

from .models import AuthorBlog, AuthorBook, Blog, BookGenre, Comment, Discussion, Group, ReaderGenre, SiteUser, Reader, Author, Book, Genre, Friendship, Message, UserBook, Review
from .forms import LoginForm, SignUpForm, UpdatePassForm, UpdateUserForm

import random
import string

from django.core.mail import send_mail


from django.utils import timezone
from datetime import timedelta


from django.core.management import call_command
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse




def generate_2fa_token():

    """Generates a random 6-digit token."""

    return ''.join(random.choices(string.digits, k=6))

def verify_2fa(request):

    """View to handle 2FA token verification and redirect user based on their type."""

    if request.method == "POST":
        token = request.POST.get('token')  # The token entered by the user
        user = request.user  # Current logged-in user

        if user.two_factor_token == token:
            # Check if the token has expired (e.g., 10 minutes)
            if timezone.now() - user.token_generated_at < timedelta(minutes=10):
                # Token is valid, log the user in and redirect to their appropriate dashboard
                user.two_factor_token = ''  # Clear the token after successful verification
                user.save()

                # Now redirect based on the user's type (Reader or Author)
                try:
                    # Check if the user is a Reader
                    reader = Reader.objects.filter(id=user.id).first()
                    if reader:
                        print(f"Redirecting Reader with ID {user.id}")
                        return redirect(settings.READER_REDIRECT_URL + f'?u={user.id}')

                    # Check if the user is an Author
                    author = Author.objects.filter(id=user.id).first()
                    if author:
                        print(f"Redirecting Author with ID {user.id}")
                        return redirect(settings.AUTHOR_REDIRECT_URL + f'?u={user.id}')

                except User.DoesNotExist:
                    # If the user doesn't exist in either table, fallback to default redirect
                    print(f"Error: User with ID {user.id} not found in Reader or Author.")
                    return redirect(settings.LOGIN_REDIRECT_URL)

                # If the user is neither a Reader nor an Author, fall back to a default redirect
                print(f"Unknown user type with ID {user.id}")
                return redirect(settings.LOGIN_REDIRECT_URL)

            else:
                return render(request, 'api/auth/verify_2fa.html', {'message': 'Token expired, please try again.'})

        else:
            return render(request, 'api/auth/verify_2fa.html', {'message': 'Invalid token, please try again.'})

    return render(request, 'api/auth/verify_2fa.html')

def login_site_user(request):

    """ Function to validate a potential registered site_user with 2FA """

    if request.method == "POST":
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            
            # Authenticate user
            user = authenticate(username=username, password=password)
            if user is not None:
                # Log the user in
                auth_login(request, user)

                # Generate and send the 2FA token if the user is authenticated
                token = generate_2fa_token()
                user.two_factor_token = token
                user.token_generated_at = timezone.now()
                user.save()

                # Send token to user's email
                send_mail(
                    'Your 2FA Login Token',
                    f'Your 2FA token is: {token}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )

                return redirect('verify_2fa')  # Redirect to a page to verify 2FA token

            else:
                return render(request, "api/auth/login.html", {"form": form, "message": 'Invalid username or password'})

    else:
        form = LoginForm()

    return render(request, "api/auth/login.html", {"form": form})

# Authenticate signup and login before Vue SPA redirect
def signup_site_user(request: HttpRequest) -> HttpResponse:

    """ Function to register a new site_user as a Reader or Author. """
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            date_of_birth = form.cleaned_data["date_of_birth"]
            password = form.cleaned_data["password"]
            user_type = form.cleaned_data["user_type"]  # Get selected user type

            existing_user = SiteUser.objects.filter(username=username).first()
            if existing_user:
                return render(request, "api/auth/signup.html", {"form": form, "message": "User already exists with that username."})

            # Debug: Log user type before user creation
            print(f"Creating a user with type: {user_type}")

            # Create either a Reader or an Author
            if user_type == "reader":
                user = Reader.objects.create_user(username=username, email=email, password=password)
                print(f"Created Reader user: {user}")
            else:  # user_type == "author"
                user = Author.objects.create_user(username=username, email=email, password=password)
                print(f"Created Author user: {user}")

            user.first_name = first_name
            user.last_name = last_name
            user.date_of_birth = date_of_birth
            user.save()

            # Debug: Log the type of the created user
            print(f"User created: {user} (Type: {type(user)})")

            auth_login(request, user)
             # Create either a Reader or an Author
            if user_type == "reader":
                return redirect(settings.READER_REDIRECT_URL + f'?u={user.id}')
            else:  # user_type == "author"
                return redirect(settings.AUTHOR_REDIRECT_URL + f'?u={user.id}')

    else:
        form = SignUpForm()
    return render(request, "api/auth/signup.html", {"form": form})



        
@login_required
# Logout user below
def logout_site_user(request: HttpRequest) -> HttpResponse:
    """ Function to logout a user. """
    auth.logout(request)
    return redirect(settings.LOGIN_URL)


User = get_user_model()
@login_required
#updates the password 
def update_password(request: HttpRequest) -> HttpResponse:
    """ Function to validate a potenital registered user. """
    if request.method == "POST":
        form = UpdatePassForm(request.POST)  # Use a form specifically for password updates
        if form.is_valid():
            password = form.cleaned_data["password"]

            try:
                if not password:
                    return JsonResponse({"error": "Password is required."}, status=400)

                # Use the currently logged-in user to update the password
                user = request.user
                user.set_password(password)  # Hash and set the new password
                user.save() 
                return redirect(settings.LOGIN_URL)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

        # Return form errors if invalid
        return render(request, "api/auth/updatePass.html", {"form": form, "errors": form.errors})

    # For GET requests, display the form
    else:
        form = UpdatePassForm()
    return render(request, "api/auth/updatePass.html", {"form": form})


@login_required
def update_username(request: HttpRequest) -> HttpResponse:
    """Function to update the username of the logged-in user."""
    if request.method == "POST":
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data["new_username"]

            try:
                # Ensure the new username is not already taken
                if User.objects.filter(username=new_username).exists():
                    return render(request, "api/auth/updateUsername.html", {"form": form, "message": "username exists already"})

                # Update the username
                user = request.user
                user.username = new_username
                user.save()

                return redirect(settings.LOGIN_URL)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

        # Render form with errors if invalid
        return render(request, "api/auth/updateUsername.html", {"form": form, "errors": form.errors})

    # For GET requests, display the form
    else:
        form = UpdateUserForm()
        return render(request, "api/auth/updateUsername.html", {"form": form})
    
#api for books below
def books_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the Books"""

    #post requests
    if request.method == 'POST':
        # Handle multipart/form-data for file upload
        title = request.POST.get('title')
        author = request.POST.get('author')
        blurb = request.POST.get('blurb')
        isbn = request.POST.get('isbn')
        cover_image = request.FILES.get('cover_image')

        book = Book.objects.create(
            title=title,
            author=author,
            blurb=blurb,
            isbn=isbn,
            cover_image=cover_image
        )
        return JsonResponse(book.as_dict(), status=201)

    #search queries
    search_query = request.GET.get("search", "").strip()
    if search_query:
        books = Book.objects.filter(Q(title__icontains=search_query) | Q(author__icontains=search_query))
    else:
        books = Book.objects.all()

    #get all requests
    return JsonResponse({"books": [book.as_dict() for book in books]}, safe=False)



def book_api(request: HttpRequest, book_id: int) -> JsonResponse:
    """API endpoint for a single book"""

    #check books exist 
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Book not found."}, status=404)

    #put request
    if request.method == 'PUT':
        if request.content_type.startswith('multipart/form-data'):
            # Update via multipart (e.g., image updates)
            title = request.POST.get('title', book.title)
            author = request.POST.get('author', book.author)
            blurb = request.POST.get('blurb', book.blurb)
            isbn = request.POST.get('isbn', book.isbn)
            cover_image = request.FILES.get('cover_image')

            book.title = title
            book.author = author
            book.blurb = blurb
            book.isbn = isbn
            if cover_image:
                book.cover_image = cover_image
            book.save()
        else:
            # Assume JSON
            data = json.loads(request.body)
            book.title = data.get("title", book.title)
            book.author = data.get("author", book.author)
            book.blurb = data.get("blurb", book.blurb)
            book.isbn = data.get("isbn", book.isbn)
            book.save()

        return JsonResponse(book.as_dict())

    #delete request
    if request.method == 'DELETE':
        book.delete()
        return JsonResponse({}, status=204)

    #get request
    return JsonResponse(book.as_dict())

# APIs for blog model below
def blogs_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the Blog"""
    

    # POST method which is the create method
    if request.method == 'POST':
        # Create a new book
        POST = json.loads(request.body)
        blog = Blog.objects.create(
            title = POST['title'],
            post = POST['post'],
            author = POST['author'],
        )
        return JsonResponse(blog.as_dict())

    #search query  
    search_query = request.GET.get("search", "").strip()
    if search_query:
        blogs = Blog.objects.filter(Q(title__icontains=search_query) | Q(author__icontains=search_query))
    else:
        blogs = Blog.objects.all()

    #get all request
    return JsonResponse({"blogs": [blog.as_dict() for blog in blogs]})

 

def blog_api(request: HttpRequest, blog_id: int) -> JsonResponse:
    """API endpoint for a single blog"""

    #check blog exists
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        return JsonResponse({"error": "Blog not found."}, status=404)

    # PUT method to update blog
    if request.method == 'PUT':
        try:
            PUT = json.loads(request.body)
            blog.title = PUT.get("title", blog.title)
            blog.post = PUT.get("post", blog.post)
            blog.author = PUT.get("author", blog.author)
            blog.save()
            return JsonResponse(blog.as_dict())
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # DELETE method to delete blog
    if request.method == 'DELETE':
        blog.delete()
        return JsonResponse({}, status=204)  # 204 No Content

    # GET blog data
    return JsonResponse(blog.as_dict())

# APIs for group model below
def groups_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the Group"""

    #post request  
    if request.method == 'POST':
        # Create a new group
        POST = json.loads(request.body)
        group = Group.objects.create(
            name=POST['name'],
        )
        return JsonResponse(group.as_dict())

    #search query
    search_query = request.GET.get("search", "").strip()
    if search_query:
        groups = Group.objects.filter(Q(name__icontains=search_query))
    else:
        groups = Group.objects.all()

    #get all request
    return JsonResponse({"groups": [group.as_dict() for group in groups]})


def group_api(request: HttpRequest, group_id: int) -> JsonResponse:
    """API endpoint for a single Group"""

    #check it exists
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return JsonResponse({"error": "Group not found."}, status=404)

    # GET group data
    return JsonResponse(group.as_dict())


# APIs for user model below
def site_users_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the SiteUsers"""

    #post request
    if request.method == 'POST':
        try:
            POST = json.loads(request.body)
            required_fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'password']
            missing_fields = [field for field in required_fields if field not in POST]
            if missing_fields:
                return JsonResponse({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=400)


            site_user = SiteUser.objects.create(
                first_name=POST['first_name'],
                last_name=POST['last_name'],
                email=POST['email'],
                date_of_birth=POST['date_of_birth'],
                password=POST['password'],
            )

            return JsonResponse(site_user.as_dict(), status=201)
    
        #general error hendler 
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # GET Method
    return JsonResponse({
        'site_users': [
            site_user.as_dict()
            for site_user in SiteUser.objects.all()
        ]
    })

def site_user_api(request: HttpRequest, user_id: int) -> JsonResponse:
    """API endpoint for a single site user"""

    #check it exists
    try:
        site_user = SiteUser.objects.get(id=user_id)
    except SiteUser.DoesNotExist:
        return JsonResponse({"error": "Site_User not found."}, status=404)

    # PUT method
    if request.method == 'PUT':
        try:
            PUT = json.loads(request.body)
            site_user.first_name = PUT.get("first_name", site_user.first_name)
            site_user.last_name = PUT.get("last_name", site_user.last_name)
            site_user.email = PUT.get("email", site_user.email)
            site_user.date_of_birth = PUT.get("date_of_birth", site_user.date_of_birth)
            site_user.password = PUT.get("password", site_user.password)

            site_user.save()
            return JsonResponse({"success": "Site User updated successfully."})
  
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # DELETE method
    if request.method == 'DELETE':
        site_user.delete()
        return JsonResponse({}, status=204)  # 204 No Content

    # GET method
    return JsonResponse(site_user.as_dict())


#reader apis below
def readers_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for all Readers"""
    
    #post method
    if request.method == 'POST':
        try:
            POST = json.loads(request.body)
            required_fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'password', 'book_count']
            missing_fields = [field for field in required_fields if field not in POST]
            if missing_fields:
                return JsonResponse({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=400)

            reader = Reader.objects.create(
                first_name=POST['first_name'],
                last_name=POST['last_name'],
                email=POST['email'],
                date_of_birth=POST['date_of_birth'],
                password=POST['password'],
                book_count=POST['book_count'],
            )

            return JsonResponse(reader.as_dict(), status=201)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    #search query    
    search_query = request.GET.get("search", "").strip()
    if search_query:
        readers = Reader.objects.filter(Q(username__icontains=search_query))
    else:
        readers = Reader.objects.all()

    #get all
    return JsonResponse({"readers": [reader.as_dict() for reader in readers]})


def reader_api(request: HttpRequest, reader_id: int) -> JsonResponse:
    """API endpoint for a single Reader"""

    #check it exists
    try:
        reader = Reader.objects.get(id=reader_id)
    except Reader.DoesNotExist:
        return JsonResponse({"error": "Reader not found."}, status=404)

    # PUT method (Update reader details)
    if request.method == 'PUT':
        try:
            PUT = json.loads(request.body)
            reader.first_name = PUT.get("first_name", reader.first_name)
            reader.last_name = PUT.get("last_name", reader.last_name)
            reader.email = PUT.get("email", reader.email)
            reader.date_of_birth = PUT.get("date_of_birth", reader.date_of_birth)
            reader.password = PUT.get("password", reader.password)
            reader.book_count = PUT.get("book_count", reader.book_count)
            reader.goal_one = PUT.get("goal_one", reader.goal_one)
            reader.goal_two = PUT.get("goal_two", reader.goal_two)
            reader.goal_three = PUT.get("goal_three", reader.goal_three)
            reader.goal_four = PUT.get("goal_four", reader.goal_four)
            reader.goal_five = PUT.get("goal_five", reader.goal_five)

            reader.save()
            return JsonResponse({"success": "Reader updated successfully."})
  
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # DELETE method (Remove reader)
    if request.method == 'DELETE':
        reader.delete()
        return JsonResponse({}, status=204)  # 204 No Content

    # GET method (Retrieve reader details)
    return JsonResponse(reader.as_dict())

#below are all author apis
def authors_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for all Authors"""
    
    #post method
    if request.method == 'POST':
        try:
            POST = json.loads(request.body)
            required_fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'password', 'biography']
            missing_fields = [field for field in required_fields if field not in POST]
            if missing_fields:
                return JsonResponse({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=400)

            author = Author.objects.create(
                first_name=POST['first_name'],
                last_name=POST['last_name'],
                email=POST['email'],
                date_of_birth=POST['date_of_birth'],
                password=POST['password'],
                biography=POST['biography'],
            )

            return JsonResponse(author.as_dict(), status=201)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    #search query    
    search_query = request.GET.get("search", "").strip()
    if search_query:
        authors = Author.objects.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query))
    else:
        authors = Author.objects.all()

    #get all 
    return JsonResponse({"authors": [author.as_dict() for author in authors]})


def author_api(request: HttpRequest, author_id: int) -> JsonResponse:
    """API endpoint for a single Author"""
    #checks it exists
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return JsonResponse({"error": "Author not found."}, status=404)

    # PUT method (Update author details)
    if request.method == 'PUT':
        try:
            PUT = json.loads(request.body)
            author.first_name = PUT.get("first_name", author.first_name)
            author.last_name = PUT.get("last_name", author.last_name)
            author.email = PUT.get("email", author.email)
            author.date_of_birth = PUT.get("date_of_birth", author.date_of_birth)
            author.password = PUT.get("password", author.password)
            author.biography = PUT.get("biography", author.biography)  

            author.save()
            return JsonResponse({"success": "Author updated successfully."})
  
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # DELETE method (Remove author)
    if request.method == 'DELETE':
        author.delete()
        return JsonResponse({}, status=204) 

    # GET method (Retrieve author details)
    return JsonResponse(author.as_dict())



# APIs for genre model below
def genres_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the genres"""

    #post method
    if request.method == 'POST':
        try:
            POST = json.loads(request.body)
            required_fields = ['type', 'description']
            missing_fields = [field for field in required_fields if field not in POST]
            if missing_fields:
                return JsonResponse({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=400)


            genre = Genre.objects.create(
                type=POST['type'],
                description=POST['description'],
            )

            return JsonResponse(genre.as_dict(), status=201)
    

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # GET all Method
    return JsonResponse({
        'genres': [
            genre.as_dict()
            for genre in Genre.objects.all()
        ]
    })

def genre_api(request: HttpRequest, genre_id: int) -> JsonResponse:
    """API endpoint for a single genre"""
    #check it exists
    try:
        genre = Genre.objects.get(id=genre_id)
    except Genre.DoesNotExist:
        return JsonResponse({"error": "Genre not found."}, status=404)

    # PUT method
    if request.method == 'PUT':
        try:
            PUT = json.loads(request.body)
            genre.type = PUT.get("type", genre.type)
            genre.description = PUT.get("description",  genre.description)
            genre.save()
            return JsonResponse({"success": "Genre updated successfully."})
  
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # DELETE method
    if request.method == 'DELETE':
        genre.delete()
        return JsonResponse({}, status=204)  # 204 No Content

    # GET method
    return JsonResponse(genre.as_dict())


# APIs for friendship model below
def friendships_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the Friendship"""

    # POST method which is the create method
    if request.method == 'POST':
        # Create a new friendship
        POST = json.loads(request.body)
        user = Reader.objects.get(id=POST.get("user_id"))
        friend = Reader.objects.get(id=POST.get("friend_id"))

        friendship = Friendship.objects.create(
            user = user,
            friend = friend,
            accepted = POST['accepted'],
        )
        return JsonResponse(friendship.as_dict())

    # GET method which allows the user to view all friendships
    return JsonResponse({
        'friendships': [
            friendship.as_dict()
            for friendship in Friendship.objects.all()
        ]
    })

def friendship_api(request: HttpRequest, friendship_id: int) -> JsonResponse:
    """API endpoint for a single friendship"""
    #check it exists
    try:
        friendship = Friendship.objects.get(id=friendship_id)
    except Friendship.DoesNotExist:
        return JsonResponse({"error": "Friendship not found."}, status=404)

    #put method
    if request.method == 'PUT':
        friendship.accepted = True
        friendship.save()
        return JsonResponse({"friendship": friendship.as_dict()})

    #delete method
    elif request.method == 'DELETE':
        friendship.delete()
        return JsonResponse({}, status=204)  

    #return friendship
    return JsonResponse(friendship.as_dict())

# APIs for message model below
def messages_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the Message"""

    # POST method which is the create method
    if request.method == 'POST':
        # Create a new message
        POST = json.loads(request.body)
        user = Reader.objects.get(id=POST.get("user"))
        friend = Reader.objects.get(id=POST.get("friend"))

        message = Message.objects.create(
            user = user,
            friend = friend,
            message = POST['message'],
        )
        return JsonResponse(message.as_dict())

    # GET method which allows the user to view all messages
    return JsonResponse({
        'messages': [
            message.as_dict()
            for message in Message.objects.all()
        ]
    })

def message_api(request: HttpRequest, message_id: int) -> JsonResponse:
    """API endpoint for a single message"""

    #check it exists
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return JsonResponse({"error": "Message not found."}, status=404)

    #delete method
    if request.method == 'DELETE':
        message.delete()
        return JsonResponse({}, status=204) 

    #get specific method
    return JsonResponse(message.as_dict())

# APIs for UserBook model below
def user_books_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the UserBook"""

    # POST method which is the create method
    if request.method == 'POST':
        # Create a new user book
        POST = json.loads(request.body)
        user = Reader.objects.get(id=POST.get("user_id"))
        book = Book.objects.get(id=POST.get("book_id"))

        user_book = UserBook.objects.create(
            user = user,
            book = book,
            status = POST['status'],
        )
        return JsonResponse(user_book.as_dict())

    # GET method which allows the user to view all userbook
    return JsonResponse({
        'user_books': [
            user_book.as_dict()
            for user_book in UserBook.objects.all()
        ]
    })

def user_book_api(request: HttpRequest, user_book_id: int) -> JsonResponse:
    """API endpoint for a single user_book"""
    #check it exists
    try:
        user_book = UserBook.objects.get(id=user_book_id)
    except UserBook.DoesNotExist:
        return JsonResponse({"error": "User Book not found."}, status=404)

    #put method
    if request.method == 'PUT':
        # Ensure the user has permission to edit user_book
        if request.user.id != user_book.user.id:
            return JsonResponse({"error": "Unauthorized to accept this user_book."}, status=403)
        PUT = json.loads(request.body)
        user_book.status = PUT.get("status", user_book.status)
        user_book.save()
        return JsonResponse({"User book": user_book.as_dict()})

    #delete method
    elif request.method == 'DELETE':
        # Ensure the user has permission to delete the user book
        if request.user.id != user_book.user.id:
            return JsonResponse({"error": "Unauthorized to delete this user_book."}, status=403)

        user_book.delete()
        return JsonResponse({}, status=204)  

    #get method
    return JsonResponse(user_book.as_dict())

# APIs for AuthorBook model below
def author_books_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the AuthorBook"""

    # POST method which is the create method
    if request.method == 'POST':
        # Create a new authorbook
        POST = json.loads(request.body)
        user = Author.objects.get(id=POST.get("user_id"))
        book = Book.objects.get(id=POST.get("book_id"))

        author_book = AuthorBook.objects.create(
            user = user,
            book = book,
        )
        return JsonResponse(author_book.as_dict())

    # GET method which allows the user to view all 
    return JsonResponse({
        'author_books': [
            author_book.as_dict()
            for author_book in AuthorBook.objects.all()
        ]
    })

def author_book_api(request: HttpRequest, author_book_id: int) -> JsonResponse:
    """API endpoint for a single author_book"""
    #check it exists
    try:
        author_book = AuthorBook.objects.get(id=author_book_id)
    except AuthorBook.DoesNotExist:
        return JsonResponse({"error": "Author Book not found."}, status=404)

    #delete method
    if request.method == 'DELETE':
        # Ensure the user has permission to delete the user book
        if request.user.id != author_book.user.id:
            return JsonResponse({"error": "Unauthorized to delete this author_book."}, status=403)

        author_book.delete()
        return JsonResponse({}, status=204)  

    #get specific author book
    return JsonResponse(author_book.as_dict())

# APIs for AuthorBlog model below
def author_blogs_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the AuthorBlog"""

    # POST method which is the create method
    if request.method == 'POST':
        # Create a new 
        POST = json.loads(request.body)
        user = Author.objects.get(id=POST.get("user_id"))
        blog = Blog.objects.get(id=POST.get("blog_id"))

        author_blog = AuthorBlog.objects.create(
            user = user,
            blog = blog,
        )
        return JsonResponse(author_blog.as_dict())

    # GET method which allows the user to view all 
    return JsonResponse({
        'author_blogs': [
            author_blog.as_dict()
            for author_blog in AuthorBlog.objects.all()
        ]
    })

def author_blog_api(request: HttpRequest, author_blog_id: int) -> JsonResponse:
    """API endpoint for a single author_blog"""
    #check it exists
    try:
        author_blog = AuthorBlog.objects.get(id=author_blog_id)
    except AuthorBlog.DoesNotExist:
        return JsonResponse({"error": "Author Blog not found."}, status=404)

    #delete method
    if request.method == 'DELETE':
        # Ensure the user has permission to delete the user book
        if request.user.id != author_blog.user.id:
            return JsonResponse({"error": "Unauthorized to delete this author_blog."}, status=403)

        author_blog.delete()
        return JsonResponse({}, status=204)  

    #get specific one
    return JsonResponse(author_blog.as_dict())


# APIs for ReaderGenre model below
def reader_genres_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the ReaderGenre"""

    # POST method which is the create method
    if request.method == 'POST':
        # Create a new readergenre
        POST = json.loads(request.body)
        user = Reader.objects.get(id=POST.get("user_id"))
        genre = Genre.objects.get(id=POST.get("genre_id"))

        reader_genre = ReaderGenre.objects.create(
            user = user,
            genre = genre,
        )
        return JsonResponse(reader_genre.as_dict())

    # GET method which allows the user to view all readergenres
    return JsonResponse({
        'reader_genre': [
            reader_genre.as_dict()
            for reader_genre in ReaderGenre.objects.all()
        ]
    })

def reader_genre_api(request: HttpRequest, reader_genre_id: int) -> JsonResponse:
    """API endpoint for a single reader_genre"""
    #check it exists
    try:
        reader_genre = ReaderGenre.objects.get(id=reader_genre_id)
    except ReaderGenre.DoesNotExist:
        return JsonResponse({"error": "Reader genre not found."}, status=404)
    
    #put method
    if request.method == 'PUT':
        # Ensure the user has permission to edit user_book
        if request.user.id != reader_genre.user.id:
            return JsonResponse({"error": "Unauthorized to accept this user_book."}, status=403)
        PUT = json.loads(request.body)
        reader_genre.count = PUT.get("count", reader_genre.count)
        reader_genre.save()
        return JsonResponse({"User book": reader_genre.as_dict()})    

    #delete method
    elif request.method == 'DELETE':
        # Ensure the user has permission to delete the user book
        if request.user.id != reader_genre.user.id:
            return JsonResponse({"error": "Unauthorized to delete this user_book."}, status=403)

        reader_genre.delete()
        return JsonResponse({}, status=204)  # 204 No Content

    #get one method
    return JsonResponse(reader_genre.as_dict())

# APIs for bookGenre model below
def book_genres_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the bookGenre"""

    # POST method which is the create method
    if request.method == 'POST':
        # Create a new book_genre
        POST = json.loads(request.body)
        book= Book.objects.get(id=POST.get("book_id"))
        genre = Genre.objects.get(id=POST.get("genre_id"))

        book_genre = BookGenre.objects.create(
            book = book,
            genre = genre,
        )
        return JsonResponse(book_genre.as_dict())

    # GET method which allows the user to view all book_genre
    return JsonResponse({
        'book_genre': [
            book_genre.as_dict()
            for book_genre in BookGenre.objects.all()
        ]
    })

def book_genre_api(request: HttpRequest, book_genre_id: int) -> JsonResponse:
    """API endpoint for a single book_genre"""

    #check it exists
    try:
        book_genre = BookGenre.objects.get(id=book_genre_id)
    except BookGenre.DoesNotExist:
        return JsonResponse({"error": "Reader genre not found."}, status=404)

    #delete method
    if request.method == 'DELETE':
        book_genre.delete()
        return JsonResponse({}, status=204)  

    #get one method
    return JsonResponse(book_genre.as_dict())

# APIs for review model below
def reviews_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the review"""

    # POST method which is the create method
    if request.method == 'POST':
        # Create a new review
        POST = json.loads(request.body)
        user = Reader.objects.get(id=POST.get("user_id"))
        book = Book.objects.get(id=POST.get("book_id"))

        review = Review.objects.create(
            user = user,
            book = book,
            title = POST['title'],
            rating = POST['rating'],
            message = POST['message'],
        )
        return JsonResponse(review.as_dict())

    # GET method which allows the user to view all reviews
    return JsonResponse({
        'reviews': [
            review.as_dict()
            for review in Review.objects.all()
        ]
    })

def review_api(request: HttpRequest, review_id: int) -> JsonResponse:
    """API endpoint for a single review"""

    #check it exists
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return JsonResponse({"error": "Review not found."}, status=404)

    #put method
    if request.method == 'PUT':
        # Ensure the user has permission to edit the review
        if request.user.id != review.user.id:
            return JsonResponse({"error": "Unauthorized to accept this review."}, status=403)

        PUT = json.loads(request.body)
        review.title = PUT.get("title", review.title)
        review.rating = PUT.get("rating", review.rating)
        review.message = PUT.get("message", review.message)
        review.save()
        return JsonResponse({"Review": review.as_dict()})

    #delete method
    elif request.method == 'DELETE':
        # Ensure the user has permission to delete this review
        if request.user.id != review.user.id:
            return JsonResponse({"error": "Unauthorized to delete this Review."}, status=403)

        review.delete()
        return JsonResponse({}, status=204)  # 204 No Content

    #get one method
    return JsonResponse(review.as_dict())

# APIs for comments model below
def comments_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the comment"""

    # POST method which is the create method
    if request.method == 'POST':
        # Create a new comment
        POST = json.loads(request.body)
        user = Reader.objects.get(id=POST.get("user_id"))
        blog = Blog.objects.get(id=POST.get("blog_id"))

        comment = Comment.objects.create(
            user = user,
            blog = blog,
            comment = POST['comment'],
        )
        return JsonResponse(comment.as_dict())

    # GET method which allows the user to view all comments
    return JsonResponse({
        'comments': [
            comment.as_dict()
            for  comment in Comment.objects.all()
        ]
    })

def comment_api(request: HttpRequest, comment_id: int) -> JsonResponse:
    """API endpoint for a single comment"""
    #check it exists
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse({"error": "Comment not found."}, status=404)

    #delete method
    if request.method == 'DELETE':
        # Ensure the user has permission to delete this comment
        if request.user.id != comment.user.id:
            return JsonResponse({"error": "Unauthorized to delete this Comment."}, status=403)

        comment.delete()
        return JsonResponse({}, status=204)  # 204 No Content

    #get a specifc one method
    return JsonResponse(comment.as_dict())

# APIs for discussions model below
def discussions_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the discussion"""

    #post method
    if request.method == 'POST':
        # Create a new discussion
        POST = json.loads(request.body)
        user = Reader.objects.get(id=POST.get("user_id"))
        group = Group.objects.get(id=POST.get("group_id"))  

        discussion = Discussion.objects.create(
            user=user,
            group=group,
            discussion=POST['discussion'],  # Renamed 'comment' to 'content'
        )
        return JsonResponse(discussion.as_dict())

    # GET method to list all discussions
    return JsonResponse({
        'discussions': [
            discussion.as_dict()
            for discussion in Discussion.objects.all()
        ]
    })


def discussion_api(request: HttpRequest, discussion_id: int) -> JsonResponse:
    """API endpoint for a single discussion"""

    #check it exists
    try:
        discussion = Discussion.objects.get(id=discussion_id)
    except Discussion.DoesNotExist:
        return JsonResponse({"error": "Discussion not found."}, status=404)

    #delete method
    if request.method == 'DELETE':
        discussion.delete()
        return JsonResponse({}, status=204)

    #get one specifc one
    return JsonResponse(discussion.as_dict())

