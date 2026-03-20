from .models import Add_Book, Review
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Add_Book_Form(forms.ModelForm): 
    class Meta:
        model = Add_Book
        fields = ("title", "author", "catagory", "description", "cover_image")
        
class SignupForm(UserCreationForm):
        
        email = forms.EmailField(required=True)
        username = forms.CharField(max_length=30, required=True)
        password1 = forms.CharField(label='Password', widget=forms.PasswordInput, max_length=50)
        password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, max_length=50)
        class Meta:
            model = User
            fields = ("username", "email", "password1", "password2")

class ReviewForm(forms.ModelForm):
    class Meta:
        model= Review
        fields = ['review', 'rating']
        widgets = {
            'review': forms.Textarea(attrs={
                'placeholder': 'Write something meaningful...',
                'class': 'w-full bg-white/5 border border-white/10 p-6 rounded-2xl h-32 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'rating': forms.HiddenInput(),
            }), # The radio buttons in HTML handle this
        }