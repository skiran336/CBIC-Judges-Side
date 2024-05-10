from django.http import HttpResponse
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

def save_data(request):
    if request.method == "POST":
        # Get the form data
        student_id = request.POST.get("_id")
        identify = request.POST.get("identify")
        impact = request.POST.get("Impact")
        competitive = request.POST.get("Competitive")
        market = request.POST.get("Market")
        viability = request.POST.get("Viability")
        strategy = request.POST.get("Strategy")
        financial = request.POST.get("Financial")
        management = request.POST.get("Management")
        presentation = request.POST.get("Presentation")

        # Convert student_id to ObjectId
        student_id = ObjectId(student_id)
        print(student_id)

        # Check if the student data already exists
        existing_student = student_collection.find_one({"_id": student_id})

        if existing_student:
            # Update the existing document in MongoDB
            student_collection.save(
                {"_id": student_id},
                {
                    "$set": {
                        "identify": identify,
                        "impact": impact,
                        "competitive": competitive,
                        "market": market,
                        "viability": viability,
                        "strategy": strategy,
                        "financial": financial,
                        "management": management,
                        "presentation": presentation
                    }
                }
            )
            return HttpResponse("Data updated successfully!")
        else:
            return HttpResponse("Student data not found")

    else:
        return HttpResponse("Invalid request method")