from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages 

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signin(request):

    return render(request, "authentication/signin.html")

def signup(request):

    if request.method == "POST":

        if 'action' in request.POST and request.POST['action'] == 'cancel':
            return redirect('signin')
        
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your Account has been succesfully created.")

        return redirect('signin')


    return render(request, "authentication/signup.html")



def signout(request):
    pass