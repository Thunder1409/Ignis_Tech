import os, cv2  # Importing necessary modules
from django.shortcuts import render, redirect, get_object_or_404  # Importing Django shortcuts
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import CreateAccountForm, SignForm, eventForm  # Importing forms and models
from .models import Signin, Event
from django.contrib import messages
from django.db import transaction

# Function to fetch data
def get_data(request):
    sql_data = Event.objects.all()  # Fetching all events from the database

    # Creating a dictionary to pass to the template
    data = {'event': eventForm(), 'sql_data': sql_data}

    # Retrieving and decrypting cookie value if exists
    my_cookie_value = request.COOKIES.get('jnl')
    if my_cookie_value:
        data['mkc'] = decrept(my_cookie_value, 69)

    return data

# Function to render the main page
def show_page(request):
    data = get_data(request)  # Fetching data
    return render(request, 'Index.html', data)  # Rendering Index.html template with fetched data

# Function to render user-specific page
def user_specific(request):
    data = get_data(request)  # Fetching data
    return render(request, 'User_specific.html', data)  # Rendering User_specific.html template with fetched data

# Function to encrypt text using Caesar cipher
def encrypt(text, s):
    result = ""
    for i in range(len(text)):
        letter = text[i]
        result += chr(ord(letter) + s * 10 % 26 + 65)
    return result

# Function to decrypt text encrypted by encrypt function
def decrept(enc_pass, s):
    result = ""
    for i in range(len(enc_pass)):
        letter = enc_pass[i]
        result += chr(ord(letter) - s * 10 % 26 - 65)
    return result

# Function to handle user login
def login_page(request):
    my_cookie_value = request.COOKIES.get('jnl')  # Retrieving cookie value
    if my_cookie_value:
        return render(request, 'Index.html', {"mkc": my_cookie_value})  # Rendering Index.html if user is already logged in

    signup_form = CreateAccountForm()  # Creating sign up form instance
    login_form = SignForm()  # Creating login form instance
    data = {'login': login_form, 'signup': signup_form}  # Data to be passed to the template

    if request.method == "POST":  # Handling POST request
        form = SignForm(request.POST)  # Creating form instance with POST data

        if form.is_valid():  # Checking if form data is valid
            user_data = form.cleaned_data  # Cleaning form data

            mysql_entry = Signin.objects.filter(email=user_data['email']).first()  # Querying user data from database
            if mysql_entry:
                if mysql_entry.password == user_data['password'] and mysql_entry.email == user_data['email']:
                    # Creating a cookie after successful login
                    mail = encrypt(user_data['email'], 69)
                    response = HttpResponseRedirect(reverse('home'))
                    response.set_cookie('jnl', mail)
                    return response  # Redirecting to home page after successful login

                else:
                    data['error'] = "Invalid Credentials"  # Error message for invalid credentials
            else:
                data['error'] = "No user found with this email. Please Signup"  # Error message for user not found

        else:
            data['error'] = "Invalid form submission. Please check your input."  # Error message for invalid form submission

    else:
        data['error'] = ""  # No error message for GET request

    return render(request, 'Login.html', data)  # Rendering Login.html with form data and error messages

# Function to handle user sign up
def sign_up(request):
    signup_form = CreateAccountForm()  # Creating sign up form instance
    login_form = SignForm()  # Creating login form instance

    data = {}  # Data to be passed to the template

    if request.method == "POST":  # Handling POST request
        signup_form = CreateAccountForm(request.POST)  # Creating form instance with POST data
        if signup_form.is_valid():  # Checking if form data is valid
            user_data = signup_form.cleaned_data  # Cleaning form data
            email = user_data.get('email')  # Extracting email from form data

            # Check if email already exists
            if Signin.objects.filter(email=email).exists():
                data['error'] = "Email already exists."  # Error message for existing email
            else:
                # Hash the password before saving (for security)
                with transaction.atomic():  # Using atomic transaction for database operation
                    user = Signin.objects.create(  # Creating user instance
                        user_name=user_data.get('name'),
                        email=email,
                        password=user_data.get('password')
                    )
                    user.save()  # Saving user data to the database
                return render(request, 'Login.html', {'login': login_form,'signup': signup_form,'message': "Account created successfully. Please log in"})

    else:
        signup_form = CreateAccountForm()  # Creating sign up form instance if not a POST request

    data['signup'] = signup_form  # Adding sign up form to data
    data['login'] = login_form  # Adding login form to data
    return render(request, 'Signup.html', data)  # Rendering Signup.html with form data

# Function to create events
def create_event(request):
    data = {'event': eventForm()}  # Creating event form instance
    data['mkc'] = request.COOKIES.get('jnl')  # Retrieving cookie value
    data['message'] = False  # Initializing message flag

    if request.method == 'POST':  # Handling POST request
        form = eventForm(request.POST, request.FILES)  # Creating form instance with POST data

        if form.is_valid():  # Checking if form data is valid
            user_id = decrept(request.COOKIES.get('jnl'), 69)  # Decrypting user ID from cookie

            # Create an event object with form data and user ID
            event = Event(
                event_name=form.cleaned_data['name'],
                event_date=form.cleaned_data['date'],
                event_time=form.cleaned_data['time'],
                event_location=form.cleaned_data['location'],
                event_image=form.cleaned_data['image'],
                user_id=user_id
            )
            event.save()  # Saving event data to the database
            data['message'] = True  # Setting message flag to True

            image_name = "media/" + str(event.event_image)  # Path to the uploaded image
            try:
                img = cv2.imread(image_name)  # Reading the uploaded image with OpenCV

                # Checking if image dimensions exceed certain values and cropping if necessary
                height, width, _ = img.shape
                if width > 1250 or height > 600:
                    crop_width = min(width, 1250)  # Calculating crop width
                    crop_height = min(height, 600)  # Calculating crop height

                    # Cropping the image
                    img_cropped = img[0:crop_height, 0:crop_width]
                    cv2.imwrite(image_name, img_cropped)  # Saving the cropped image
                    print("Image cropped")

            except SyntaxWarning as e:
                print("Error -: ", e)  # Handling exceptions during image processing

    return redirect(reverse('home'))  # Redirecting to home page

# Function to handle liking an event
def like_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)  # Getting the event object
    event.is_liked = True  # Setting is_liked attribute to True
    event.save()  # Saving the event object
    return redirect(reverse('home'))  # Redirecting to home page
