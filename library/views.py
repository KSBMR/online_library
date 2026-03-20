
from urllib import request
from django.contrib.auth.models import User
from django.db.models import Q # search query

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import Add_Book_Form, SignupForm, ReviewForm
from .models import Add_Book, Review

from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
# Create your views here.

def home(request):
    add_book = Add_Book.objects.all()
    # re_views= add_book.reviews.all()

    #search query
    query = request.GET.get('q')
    if query:
        add_book = add_book.filter(
            Q(title__icontains = query)|
            Q(author__icontains = query)
        )

    catagory_filter = request.GET.get('catagory')
    if catagory_filter:
        add_book = add_book.filter(catagory__iexact = catagory_filter)

    catagories = Add_Book.objects.values_list('catagory', flat = True).distinct()

    context = {
        'add_book': add_book, 
        'catagories': catagories,
        'catagories_filter': catagory_filter,
        'query': query,
    }
    
    return render(request, 'library/home.html', context)


def add_book(request):
    if request.method == 'POST':
        form = Add_Book_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = Add_Book_Form()
    return render(request, 'form/addbook.html', {'add_book': form})


# def book_detail(request, pk):
#     book = get_object_or_404(Add_Book, pk=pk)
#     return render(request, 'form/book_detail.html', {'book': book})


def signupform(request):
    if request.method == 'POST':
        data = request.POST
        form = SignupForm(data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home') 
        else:
            messages.error(request,'User already exists.')
          
    else:
        form = SignupForm()

    return render(request, 'form/signup.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {username}!")
                return redirect('home')
        else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    context={
            'form':form
        }
    return render(request, 'form/login.html', context)
    

def user_logout(request):
    logout(request)
    return redirect('home')

# @login_required
# def bookview(request, pk):
#     books = get_object_or_404(Add_Book, pk=pk)
#     return render(request, 'library/bookview.html', {'books': books})

@login_required
def bookview(request, pk):
    # Fetch the book or return 404
    books = get_object_or_404(Add_Book, pk=pk)

    # Get all reviews for this book (using the related_name='reviews')
    reviews = books.reviews.all().order_by('-id')   # newest first

    # Initialize the form
    form = ReviewForm()

    #Average rating calculation, aggregate 
    average_rating = reviews.aggregate(
        avg = Avg('rating') or 0,
        count = Count('id') or 0
    )

    # Handle POST (review submission)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = books
            review.save()
            messages.success(request, 'Your review has been added!')
            # Redirect to the same page to show the new review
            return redirect('bookview', pk=books.pk)
        else:
            messages.error(request, 'Please correct the errors below.')

    context = {
        'books': books,        # matches the variable name used in your template
        'reviews': reviews,
        'form': form,
        'average_rating': average_rating,
    }
    return render(request, 'library/bookview.html', context)


def delete_book(request, pk):
    book =get_object_or_404(Add_Book, pk=pk)
    book.delete()
    return redirect('home')


