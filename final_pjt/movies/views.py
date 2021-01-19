from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q

from .models import Movie, Genre

from django.contrib.auth import get_user_model
User = get_user_model()

def home(request):
    movies = Movie.objects.order_by('?')
    movies_top = Movie.objects.order_by('?')[0]
    movies_top7 = Movie.objects.order_by('?')[1:7]
    paginator = Paginator(movies, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'movies' : movies,
        'movies_top' : movies_top,
        'movies_top7' : movies_top7,
        'page_obj' : page_obj,
    }

    return render(request, 'movies/home.html', context)


def search(request):
    movie_lst = Movie.objects.all()
    word = request.GET.get('word', '')
    failure = None


    if word:
        movie_lst = Movie.objects.filter(Q(title__icontains=word) | Q(original_title__icontains=word))

        if movie_lst:
            movies_top = movie_lst[0]
            if len(movie_lst) > 1:
                movies_tops = movie_lst[1:]
            else:
                movies_tops = []

            paginator = Paginator(movie_lst, 12)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {
                'movie_lst': movie_lst,
                'word': word,
                'movies_top' : movies_top,
                'movies_tops' : movies_tops,
                'failure': failure,
                'page_obj' : page_obj,
            }

            return render(request, 'movies/search.html', context)

        else:
            failure = '검색 관련 영화가 존재하지 않습니다.'

    context = {
        'movie_lst': movie_lst,
        'word': word,
        # 'movies_top' : movies_top,
        # 'movies_tops' : movies_tops,
        'failure': failure,
    }

    return render(request, 'movies/search.html', context)


def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    context = {
        'movie' : movie,
    }

    return render(request, 'movies/detail.html', context)


def related_reviews(request, movie_pk):
    movie = Movie.objects.get(id=movie_pk)
    review_lst = movie.review_movie.all()
    paginator = Paginator(review_lst, 12)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'movie': movie,
        'review_lst': review_lst,
        'page_obj': page_obj,
    }

    return render(request, 'movies/related_review.html', context)


def like(request, movie_pk):
    user = request.user
    movies = get_object_or_404(Movie, pk=movie_pk)

    if movies.like_users.filter(pk=user.pk).exists():
        movies.like_users.remove(user)
        liked = False
    else:
        movies.like_users.add(user)
        liked = True

    context = {
        'liked': liked,
    }

    return JsonResponse(context)


def latest(request):
    movies = Movie.objects.order_by('-release_date')
    movies_top = Movie.objects.order_by('-release_date')[0]
    movies_top7 = Movie.objects.order_by('-release_date')[1:7]
    paginator = Paginator(movies, 12)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'movies' : movies,
        'movies_top' : movies_top,
        'movies_top7' : movies_top7,
        'page_obj' : page_obj,
    }

    return render(request, 'movies/release.html', context)

def ranked(request):
    movies = Movie.objects.order_by('-vote_average')
    movies_top = Movie.objects.order_by('-vote_average')[0]
    movies_top7 = Movie.objects.order_by('-vote_average')[1:7]
    paginator = Paginator(movies, 12)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'movies' : movies,
        'movies_top' : movies_top,
        'movies_top7' : movies_top7,
        'page_obj' : page_obj,
    }

    return render(request, 'movies/rank.html', context)

def popular(request):
    movies = Movie.objects.order_by('-popularity')
    movies_top = Movie.objects.order_by('-popularity')[0]
    movies_top7 = Movie.objects.order_by('-popularity')[1:7]
    paginator = Paginator(movies, 12)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'movies' : movies,
        'movies_top' : movies_top,
        'movies_top7' : movies_top7,
        'page_obj' : page_obj,
    }

    return render(request, 'movies/popularity.html', context)

@login_required
def recommend(request):
    movies = Movie.objects.filter(like_users=request.user).all()
    recommend_list = []
    # 좋아요를 누른 영화가 있을 때
    if len(movies) > 0:
        # 카카오 비전 API 기반으로 영화 추천
        for com_movie in Movie.objects.all():
            count = 0
            if Image_information.objects.filter(pk=com_movie.pk):
                com_img_info = Image_information.objects.filter(pk=com_movie.pk)[0]
            else:
                continue
            for movie in movies:
                if com_movie.pk == movie.pk:
                    continue
                image_information = Image_information.objects.get(pk=movie.pk)
                for tag in image_information.tag.all():
                    for com_tag in com_img_info.tag.all():
                        if tag.pk == com_tag.pk:
                            count += 1
                if count > 10:
                    recommend_list.append(com_movie)
                    break
            if len(recommend_list) > 30:
                break
    # 좋아요 한 영화의 정보가 부족할시 회원가입때 선택한 장르를 기반으로 영화 추천
    if len(recommend_list) < 3:
        movies = Movie.objects.all()
        for user_genre in request.user.like_genres.all():
            for movie in movies:
                for movie_genre in movie.genres.all():
                    if user_genre.pk == movie_genre.pk:
                        recommend_list.append(movie)
                        break
                if len(recommend_list) > 30:
                    break
    
    movies_top = random.choice(recommend_list)
    recommend_list.pop(recommend_list.index(movies_top))
    movies_top2 = random.sample(recommend_list, 2)

    context = {
        'movies_top' : movies_top,
        'movies_top2' : movies_top2,
    }
    
    return render(request, 'movies/recommend.html', context)