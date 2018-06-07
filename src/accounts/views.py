from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from .forms import LoginForm, RegisterForm
from django.utils.http import is_safe_url

def logout_page(request):
    logout(request)
    return redirect('/login/')

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
            "title" : "Login page...",
            "form"  : form
        }
    print("User logged in")
    print(request.user.is_authenticated())

    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post

    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username = username, password = password)
        print(user)
        if user is not None:
            print(request.user.is_authenticated())
            login(request, user)
            print(redirect_path)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                # A backend authenticated the credentials
                # Redirect to a success page.
                #context['form'] = LoginForm()
                return redirect("/")
        else:
            # No backend authenticated the credentials
            print("Error")
            
    return render(request,"accounts/login.html", context)

User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
            "title" : "Register page...",
            "form"  : form
        }
    if form.is_valid():
        print("form is valid")
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create_user(username,email,password,)
        print(new_user)
    return render(request, "accounts/register.html", context)
