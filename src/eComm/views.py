from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from .forms import ContactForm, LoginForm, RegisterForm

def home_page(request):
    context = {
        "title":"This is title replacement....."
    }
    return render(request, "home_page.html", context)
    #return HttpResponse()

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
            "title" : "Login page...",
            "form"  : form
        }
    print("User logged in")
    print(request.user.is_authenticated())
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username = username, password = password)
        print(user)
        if user is not None:
            print(request.user.is_authenticated())
            login(request, user)
            # A backend authenticated the credentials
            # Redirect to a success page.
            #context['form'] = LoginForm()
            return redirect("/login")
        else:
            # No backend authenticated the credentials
            print("Error")
            
    return render(request,"auth/login.html", context)

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
    return render(request, "auth/register.html", context)

  
def about_page(request):
    return render(request, "about_page.html", {})

def contact_page(request):
    form = ContactForm()#request.POST or None)
    context = {
            "title" : "Contact page...",
            "form"  : form
        }
    
#     if form.is_valid():
#         print(form.cleaned_data)
    
    if request.method == "POST":
        print(request.POST)
        print(request.POST.get('fullname'))
        print(request.POST.get('email'))
        print(request.POST.get('content'))
    return render(request, "contact/view.html", context)