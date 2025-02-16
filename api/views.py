import json
from django.conf import settings
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .models import Book, SiteUser
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
            site_user = auth.authenticate(username=username, password=password)
            # Rendering Vue SPA if site_user is found
            if site_user is not None:
                auth.login(request, site_user)
                # Saving user id in variable to add to redirect as query
                site_user_id=site_user.id
                return redirect(settings.LOGIN_REDIRECT_URL+'?u=%s' %site_user_id)
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
            site_user = auth.authenticate(username=username, password=password)
            # Rendering Vue SPA if an existing site_user is not found
            if site_user is None:
                # Create a new site_user with input form details
                site_user = SiteUser.objects.create_user(username=username, email=email, password=password)
                site_user.first_name=first_name
                site_user.last_name=last_name
                site_user.date_of_birth=date_of_birth
                site_user.save()

                auth.login(request, site_user)
                site_user_id=site_user.id
                return redirect(settings.LOGIN_REDIRECT_URL+'?u=%s' %site_user_id)
            else:
                # Show failed user creation
                return render(request, "api/auth/signup.html", {"form": form, "message": 'Site_User already exists with that username. Please try again.'})
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

    # GET method which allows the user to view all hobbies
    return JsonResponse({
        'books': [
            book.as_dict()
            for book in Book.objects.all()
        ]
    })

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