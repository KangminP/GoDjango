from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.utils import timezone
from django.core.paginator import Paginator

from .models import Message
from .forms import CustomUserCreationForm, MessageForm
from django.contrib.auth import get_user_model
from movies.models import Genre

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            genre = get_object_or_404(Genre, pk=int(user.pick))
            user.like_genres.add(genre)
            auth_login(request, user)
            return redirect('movies:home')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'movies:home')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('movies:home')

@login_required
def photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.owner = request.user
            photo.pub_date = timezone.now()
            photo.save()
            pass
            # return redirect()
    else:
        form = PhotoForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/photo.html', context)


@login_required
def profile(request):
    user = request.user
    my = User.objects.get(id=user.pk)
    my_movies = my.like_movies.all()
    my_reviews = my.like_reviews.all()

    if my_movies and my_reviews:
            
        paginator = Paginator(my_movies, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        paginator = Paginator(my_reviews, 5)
        page_number = request.GET.get('page')
        page_obj2 = paginator.get_page(page_number)
        
        context = {
            'my_movies': my_movies,
            'my_reviews': my_reviews,
            'page_obj': page_obj,
            'page_obj2': page_obj2,
        }
        
        return render(request, 'accounts/my_movies.html', context)

    elif my_movies and not my_reviews:
        paginator = Paginator(my_movies, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'my_movies': my_movies,
            'page_obj': page_obj,
        }

        return render(request, 'accounts/my_movies.html', context)

    elif not my_movies and my_reviews:
        paginator = Paginator(my_reviews, 10)
        page_number = request.GET.get('page')
        page_obj2 = paginator.get_page(page_number)

        context = {
            'my_reviews': my_reviews,
            'page_obj2': page_obj2,
        }

        return render(request, 'accounts/my_movies.html', context)

    return render(request, 'accounts/my_movies.html')



@login_required
def list_msg(request):
    received_list = Message.objects.filter(receive_user=request.user)
    sent_list = Message.objects.filter(send_user=request.user)


    context = {
        'received_list': received_list,
        'sent_list': sent_list,
    }

    return render(request, 'accounts/message_list.html', context)

@login_required
def send_msg(request, user_pk):
    receive_user = get_object_or_404(User, pk=user_pk)
    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.send_user = request.user
            message.receive_user = receive_user
            message.content = message_form.cleaned_data.get("content")
            message.save()
            return redirect('messaos:list_msg')
    else:
        message_form = MessageForm()

    context = {
        'receive_user': receive_user,
        'message_form': message_form,
    }

    return render(request, 'accounts/message_send.html', context)


@login_required
def delete_msg(request, message_pk):
    message = get_object_or_404(Message, pk=message_pk)
    message.delete()

    return redirect('accounts:list_msg')