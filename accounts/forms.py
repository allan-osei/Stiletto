from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput
from django import forms

from .models import CustomUser

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class":"input", 'id':"password1", "placeholder":"a"}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"class":"input", 'id':"password2", "placeholder":"a "}),
    )

    
    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_no")
        widgets = {
            "username": TextInput(attrs={"class":"input", 'id':"userName", "placeholder":"a"}),
            "email": TextInput(attrs={"class":"input", 'id':"email", "placeholder":"a"}),
            "phone_no": TextInput(attrs={"class":"input", 'id':"phoneNumber", "placeholder":"a"}),
        }

class LogInForm(forms.Form):
    email = forms.EmailField(widget=TextInput(attrs={"class":"input", "id":"floatingInput", "placeholder":"name@example.com"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"input", "id":"Password", "placeholder":"Password","style":"width:90%;"}))