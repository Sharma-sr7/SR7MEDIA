from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home_url')
    if request.method == "POST":
        user = authenticate(username=request.POST["username"],password=request.POST["password"])
        if user is not None:
            login(request,user)
            return redirect('home_url')
        else:
            messages.error(request,"Invalid username or password")
            return redirect('login_url')

    return render(request,'login.html')

@login_required(login_url='login_url')
def logout_page(request):
    logout(request)
    return redirect('login_url')


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home_url')
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email is alredy exists")
                return redirect('register_url')
            elif User.objects.filter(username=username).exists():
                messages.info(request,"Username alredy taken by someone")
                return redirect('register_url')
            else:
                user = User.objects.create_user(username=username,email=email,password=password1)
                user.save()
                
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect("login_url")
        else:
            messages.info(request,"Password Not Matching")

    return render(request,'register.html')