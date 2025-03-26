import json
from django.conf import settings
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q


from .models import SiteUser, Reader, Author, Book, Genre, Friendship, Message, UserBook, Review
from .forms import LoginForm, SignUpForm

# Authenticate login before Vue SPA redirect
def login_site_user(request: HttpRequest) -> HttpResponse:
    """ Function to validate a potenital registered site_user. """
    if request.method == "POST":
        form = LoginForm(request.POST)
        # Clean values if valid and authenticate
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            reader = auth.authenticate(username=username, password=password)
            # Rendering Vue SPA if site_user is found
            if reader is not None:
                auth.login(request, reader)
                # Saving user id in variable to add to redirect as query
                reader_id=reader.id
                return redirect(settings.LOGIN_REDIRECT_URL+'?u=%s' %reader_id)
            else:
                # Show failed authentication
                return render(request, "api/auth/login.html", {"form": form, "message": 'Username or password invalid, please try again.'})
    else:
        form = LoginForm()
    return render(request, "api/auth/login.html", {"form": form})


# Authenticate signup and login before Vue SPA redirect
def signup_site_user(request: HttpRequest) -> HttpResponse:
    """ Function to register a new site_user. """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        # Clean values if valid and authenticate
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            date_of_birth=form.cleaned_data["date_of_birth"]
            password=form.cleaned_data["password"]
            reader = auth.authenticate(username=username, password=password)
            # Rendering Vue SPA if an existing site_user is not found
            if reader is None:
                # Create a new site_user with input form details
                reader = Reader.objects.create_user(username=username, email=email, password=password)
                reader.first_name=first_name
                reader.last_name=last_name
                reader.date_of_birth=date_of_birth
                reader.save()

                auth.login(request, reader)
                reader_id=reader.id
                return redirect(settings.LOGIN_REDIRECT_URL+'?u=%s' %reader_id)
            else:
                # Show failed user creation
                return render(request, "api/auth/signup.html", {"form": form, "message": 'Reader already exists with that username. Please try again.'})
    else:
        form = SignUpForm()
    return render(request, "api/auth/signup.html", {"form": form})
        
@login_required
# Logout user below
def logout_site_user(request: HttpRequest) -> HttpResponse:
    """ Function to logout a user. """
    auth.logout(request)
    return redirect(settings.LOGIN_URL)

# APIs for book model below
def books_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the Book"""
    

    # POST method which is the create method
    if request.method == 'POST':
        # Create a new book
        POST = json.loads(request.body)
        book = Book.objects.create(
            title = POST['title'],
            author = POST['author'],
            blurb = POST['blurb'],
            isbn = POST['isbn'],
        )
        return JsonResponse(book.as_dict())
    
    search_query = request.GET.get("search", "").strip()
    if search_query:
        books = Book.objects.filter(Q(title__icontains=search_query) | Q(author__icontains=search_query))
    else:
        books = Book.objects.all()

    return JsonResponse({"books": [book.as_dict() for book in books]})

 

def book_api(request: HttpRequest, book_id: int) -> JsonResponse:
    """API endpoint for a single book"""
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Book not found."}, status=404)

    # PUT method to update book
    if request.method == 'PUT':
        try:
            PUT = json.loads(request.body)
            book.title = PUT.get("title", book.title)
            book.author = PUT.get("author", book.author)
            book.blurb = PUT.get("blurb", book.blurb)
            book.isbn = PUT.get("isbn", book.isbn)
            book.save()
            return JsonResponse(book.as_dict())
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # DELETE method to delete book
    if request.method == 'DELETE':
        book.delete()
        return JsonResponse({}, status=204)  # 204 No Content

    # GET book data
    return JsonResponse(book.as_dict())

# APIs for user model below
def site_users_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the SiteUsers"""

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
        return JsonResponse({})

    # GET method
    return JsonResponse(site_user.as_dict())



def readers_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for all Readers"""
    
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
        
    search_query = request.GET.get("search", "").strip()
    if search_query:
        readers = Reader.objects.filter(Q(username__icontains=search_query))
    else:
        readers = Reader.objects.all()

    return JsonResponse({"readers": [reader.as_dict() for reader in readers]})


def reader_api(request: HttpRequest, reader_id: int) -> JsonResponse:
    """API endpoint for a single Reader"""
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

            reader.save()
            return JsonResponse({"success": "Reader updated successfully."})
  
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # DELETE method (Remove reader)
    if request.method == 'DELETE':
        reader.delete()
        return JsonResponse({})

    # GET method (Retrieve reader details)
    return JsonResponse(reader.as_dict())

def authors_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for all Authors"""
    
    if request.method == 'POST':
        try:
            POST = json.loads(request.body)
            required_fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'password', 'book_count']
            missing_fields = [field for field in required_fields if field not in POST]
            if missing_fields:
                return JsonResponse({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=400)

            author = Author.objects.create(
                first_name=POST['first_name'],
                last_name=POST['last_name'],
                email=POST['email'],
                date_of_birth=POST['date_of_birth'],
                password=POST['password'],
            )

            return JsonResponse(author.as_dict(), status=201)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # GET method (List all authors)
    return JsonResponse({
        'authors': [
            author.as_dict()
            for author in Author.objects.all()
        ]
    })


def author_api(request: HttpRequest, author_id: int) -> JsonResponse:
    """API endpoint for a single Author"""
    try:
        author = Author.objects.get(id=author_id)
    except AZuthor.DoesNotExist:
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

            author.save()
            return JsonResponse({"success": "Author updated successfully."})
  
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # DELETE method (Remove author)
    if request.method == 'DELETE':
        author.delete()
        return JsonResponse({})

    # GET method (Retrieve author details)
    return JsonResponse(author.as_dict())



# APIs for genre model below
def genres_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the SiteUsers"""

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
    
        #general error hendler 
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # GET Method
    return JsonResponse({
        'genres': [
            genre.as_dict()
            for genre in Genre.objects.all()
        ]
    })

def genre_api(request: HttpRequest, genre_id: int) -> JsonResponse:
    """API endpoint for a single genre"""
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
        return JsonResponse({})

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

    # GET method which allows the user to view all hobbies
    return JsonResponse({
        'friendships': [
            friendship.as_dict()
            for friendship in Friendship.objects.all()
        ]
    })

def friendship_api(request: HttpRequest, friendship_id: int) -> JsonResponse:
    """API endpoint for a single friendship"""
    try:
        friendship = Friendship.objects.get(id=friendship_id)
    except Friendship.DoesNotExist:
        return JsonResponse({"error": "Friendship not found."}, status=404)

    if request.method == 'PUT':
        # Ensure the user has permission to accept the friendship
        if request.user.id != friendship.friend.id:
            return JsonResponse({"error": "Unauthorized to accept this friendship."}, status=403)

        friendship.accepted = True
        friendship.save()
        return JsonResponse({"friendship": friendship.as_dict()})

    elif request.method == 'DELETE':
        # Ensure the user has permission to delete the friendship
        if request.user.id != friendship.user.id and request.user.id != friendship.friend.id:
            return JsonResponse({"error": "Unauthorized to delete this friendship."}, status=403)

        friendship.delete()
        return JsonResponse({}, status=204)  # 204 No Content

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

    # GET method which allows the user to view all hobbies
    return JsonResponse({
        'messages': [
            message.as_dict()
            for message in Message.objects.all()
        ]
    })

def message_api(request: HttpRequest, message_id: int) -> JsonResponse:
    """API endpoint for a single friendship"""
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return JsonResponse({"error": "Message not found."}, status=404)

    if request.method == 'PUT':
        # Ensure the user has permission to accept the friendship
        # if request.user.id != friendship.friend.id:
        #     return JsonResponse({"error": "Unauthorized to accept this friendship."}, status=403)

        message.message = PUT.get("message", message.message)
        message.save()
        return JsonResponse({"message": message.as_dict()})

    elif request.method == 'DELETE':
        # Ensure the user has permission to delete the friendship
        # if request.user.id != friendship.user.id and request.user.id != friendship.friend.id:
        #     return JsonResponse({"error": "Unauthorized to delete this friendship."}, status=403)

        message.delete()
        return JsonResponse({}, status=204)  # 204 No Content

    return JsonResponse(message.as_dict())

# APIs for UserBook model below
def user_books_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the UserBook"""

    # POST method which is the create method
    if request.method == 'POST':
        # Create a new friendship
        POST = json.loads(request.body)
        user = Reader.objects.get(id=POST.get("user_id"))
        book = Book.objects.get(id=POST.get("book_id"))

        user_book = UserBook.objects.create(
            user = user,
            book = book,
            status = POST['status'],
        )
        return JsonResponse(user_book.as_dict())

    # GET method which allows the user to view all hobbies
    return JsonResponse({
        'user_books': [
            user_book.as_dict()
            for user_book in UserBook.objects.all()
        ]
    })

def user_book_api(request: HttpRequest, user_book_id: int) -> JsonResponse:
    """API endpoint for a single user_book"""
    try:
        user_book = UserBook.objects.get(id=user_book_id)
    except UserBook.DoesNotExist:
        return JsonResponse({"error": "User Book not found."}, status=404)

    if request.method == 'PUT':
        # Ensure the user has permission to edit user_book
        if request.user.id != user_book.user.id:
            return JsonResponse({"error": "Unauthorized to accept this user_book."}, status=403)
        PUT = json.loads(request.body)
        user_book.status = PUT.get("status", user_book.status)
        user_book.save()
        return JsonResponse({"User book": user_book.as_dict()})

    elif request.method == 'DELETE':
        # Ensure the user has permission to delete the user book
        if request.user.id != user_book.user.id:
            return JsonResponse({"error": "Unauthorized to delete this user_book."}, status=403)

        user_book.delete()
        return JsonResponse({}, status=204)  # 204 No Content

    return JsonResponse(user_book.as_dict())

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

    # GET method which allows the user to view all hobbies
    return JsonResponse({
        'reviews': [
            review.as_dict()
            for review in Review.objects.all()
        ]
    })

def review_api(request: HttpRequest, review_id: int) -> JsonResponse:
    """API endpoint for a single review"""
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return JsonResponse({"error": "Review not found."}, status=404)

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

    elif request.method == 'DELETE':
        # Ensure the user has permission to delete this review
        if request.user.id != review.user.id:
            return JsonResponse({"error": "Unauthorized to delete this Review."}, status=403)

        review.delete()
        return JsonResponse({}, status=204)  # 204 No Content

    return JsonResponse(review.as_dict())