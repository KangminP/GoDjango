from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator

from .forms import ReviewForm, CommentForm
from .models import Review, Comment
from movies.models import Movie
from django.db.models import Q

@login_required
def index(request):
    reviews = Review.objects.order_by('-pk')
    paginator = Paginator(reviews, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'reviews' : reviews,
        'page_obj' : page_obj,
    }
    return render(request, 'reviews/review_list.html', context)

@login_required
def movie_search(request):
    if request.method == 'POST':
        movie_pk = request.POST.get('movie_pk')
        return redirect('reviews:create_review', int(movie_pk))
    return render(request, 'reviews/movie_search.html')

def movie_search_modal(request):
    search_value = request.GET.get('inputText')
    movies = Movie.objects.filter(title__icontains=search_value)

    data = {}

    for movie in movies:
        data[f'{movie.pk}'] = movie.title

    return JsonResponse(data)

@login_required
def create_review(request, movie_pk):
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.movie_id = movie_pk
            review.review_user = request.user
            review.save()
            return redirect('reviews:detail_review', review.pk)
    else:
        review_form = ReviewForm()

    context = {
        'review_form' : review_form,
    }

    return render(request, 'reviews/review_create.html', context)

def detail_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm()

    context = {
        'review' : review,
        'comment_form': comment_form,
    }

    return render(request, 'reviews/review_detail.html', context)

def like(request, review_pk):
    user = request.user
    review = get_object_or_404(Review, pk=review_pk)

    if review.like_users.filter(pk=user.pk).exists():
        review.like_users.remove(user)
        liked = False
    else:
        review.like_users.add(user)
        liked = True

    context = {
        'liked': liked,
    }

    return JsonResponse(context)


@login_required
def update_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.review_user:
        if request.method == 'POST':
                review_form = ReviewForm(request.POST, instance=review)
                if review_form.is_valid():
                    review = review_form.save()
                    return redirect('reviews:detail_review', review.pk)
        else:
            review_form = ReviewForm(instance=review)
            context = {
                'review' : review,
                'review_form' : review_form,
            }
            return render(request, 'reviews/review_create.html', context)
    else:
        return redirect('reviews:detail_review', review.pk)

@login_required
def delete_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.review_user:
        review.delete()
    return redirect('reviews:index')

@login_required
def create_comment(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.review = review
            comment.comment_user = request.user
            comment.save()
        return redirect('reviews:detail_review', review.pk)
    else:
        return redirect('accounts:login')

@login_required
def delete_comment(request, review_pk, comment_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'POST':
        if request.user == comment.comment_user:
            comment.delete()
        return redirect('reviews:detail_review', review.pk)
    else:
        return redirect('accounts:login')

def search_review(request):
    review_lst = Review.objects.all()
    word = request.GET.get('word', '')
    failure = None

    if word:
        review_lst = Review.objects.filter(Q(title__icontains=word) | Q(content__icontains=word))
        if review_lst:
            paginator = Paginator(review_lst, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {
                'review_lst': review_lst,
                'word': word,
                'failure': failure,
                'page_obj' : page_obj,
            }
            return render(request, 'reviews/review_search.html', context)
        else:
            failure = '검색 관련 게시글이 존재하지 않습니다.'
    context = {
        'review_lst': review_lst,
        'word': word,
        'failure': failure,
    }
    return render(request, 'reviews/review_search.html', context)