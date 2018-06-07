from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .forms import ContactForm

def home_page(request):
    context = {
        "title":"This is title replacement....."
    }
    return render(request, "home_page.html", context)
    #return HttpResponse()

  
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