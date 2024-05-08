from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from db_connection import student_collection
from bson import ObjectId
# Create your views here.

def home(request):
    
    if request.method == 'POST':
        # Get the student ID from the form
        student_id = request.POST.get('student_id')

        # Fetch the student document from MongoDB
        student = student_collection.find_one({'_id': ObjectId(student_id)})

        # Update the student document with the submitted scores
        student.update({
            'identify_score': int(request.POST.get('identify', 0)),
            'impact_score': int(request.POST.get('Impact', 0)),
            'competitive_score': int(request.POST.get('Competitive', 0)),
            'market_score': int(request.POST.get('Market', 0)),
            'viability_score': int(request.POST.get('Viability', 0)),
            'strategy_score': int(request.POST.get('Strategy', 0)),
            'financial_score': int(request.POST.get('Financial', 0)),
            'management_score': int(request.POST.get('Management', 0)),
            'presentation_score': int(request.POST.get('Presentation', 0)),
        })

        # Save the updated student document back to MongoDB
        student_collection.save(student)

        # Optionally, you can display a success message
        messages.success(request, 'Scores submitted successfully.')

        # Redirect to the same page to avoid form resubmission on refresh
        return redirect('home')
    else:
        # If it's not a POST request, just fetch the student documents
        documents = student_collection.find()

    return render(request, "authentication/home.html", {'students': documents} )

def scorepage(request):
    return render(request, "authentication/scorepage.html")

def signup(request):

    if request.method == "POST":
        if 'action' in request.POST and request.POST['action'] == 'cancel':
            return redirect('signin')

        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if password != cpassword:
            messages.error(request, "Passwords do not match.")
            return render(request, "authentication/signup.html")

        if password is not None:
             try:
                 validate_password(password)
             except ValidationError as e:
                  for error in e.messages:
                   messages.error(request, error)

        try:
            myuser = User.objects.create_user(username=username, email=email, password=password)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request, "Your account has been successfully created.")
            return redirect('signin')
        except IntegrityError as e:
             messages.error(request, "A user with that username already exists.")
             return render(request, "authentication/signup.html")
        except Exception as e:
              messages.error(request, "Error creating account: %s" % str(e))
              return render(request, "authentication/signup.html")

    return render(request, "authentication/signup.html")

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            fname = user.first_name
            documents = student_collection.find()
            return render(request, "authentication/home.html", {'fname': fname,'students': documents})
        else:
            messages.error(request, "Bad Credentials!")

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    return redirect('signin')

