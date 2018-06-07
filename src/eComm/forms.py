from django import forms
from django.contrib.auth import get_user_model 

User = get_user_model()

class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control", 
            "placeholder": "Name"}
        )
    )
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            "class": "form-control", 
            "placeholder": "Email"}
        )
    )
    content = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control", 
            "placeholder": "Content"}
        )
    )
    
#     def clean_content(self):
#         email = self.cleaned_data.get("email")
#   

