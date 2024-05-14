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
     success_message = None
     if request.method == "POST":
        # Get the form data
        student_email = request.POST.get("student_email")
        identify = int(request.POST.get("identify", 0))
        impact = int(request.POST.get("Impact", 0))
        competitive = int(request.POST.get("Competitive", 0))
        market = int(request.POST.get("Market", 0))
        viability = int(request.POST.get("Viability", 0))
        strategy = int(request.POST.get("Strategy", 0))
        financial = int(request.POST.get("Financial", 0))
        management = int(request.POST.get("Management", 0))
        presentation = int(request.POST.get("Presentation", 0))
        
        total_score = identify + impact + competitive + market + viability + strategy + financial + management + presentation

        # Update the existing document in MongoDB
        update_query = {
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
            },
            "$inc": {
                "total_score": total_score
            }
        }
        # Execute the update query
        result = student_collection.update_one(
            {"email": student_email},
            update_query,
            upsert=True  # Create new document if not exists
        )

        if result.modified_count > 0 or result.upserted_id is not None:
            success_message = "Data updated successfully!"

     return render(request, "authentication/home.html", {'students': documents,"success_message": success_message} )

def scorepage(request):
    documents = student_collection.find()

    return render(request, "authentication/scorepage.html",{'students': documents})

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


