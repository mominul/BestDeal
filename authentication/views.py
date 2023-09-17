from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

#User Login
def login_page(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['psw']

            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    return redirect("#")
                
                else:
                    messages.error(request, "Incorrect password!")
                    print("Incorrect Paass")
            else:
                print("Unknown email, please sign up first!")
                return redirect('/signup')

        return render(request, 'login.html')
    return redirect('/')


#User Logout
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, 'logout.html')


#User new account creation
def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            # Use the email's username
            username = email.split('@')[0]
            password1 = request.POST['psw']
            password2 = request.POST['psw-repeat']
            
            if User.objects.filter(email=email):
                print("Emali already registered!")
                return redirect('/signup')
                        
            if password1 != password2:
                print("Password didn't match!")
                return redirect('/signup')

            newuser = User.objects.create_user(username, email, password1, first_name=fname, last_name=lname)
            # newuser.is_active = False
            newuser.save()
            print("Your Account has been successfully created.")
            return redirect('/')
    return render(request, "signup.html")
