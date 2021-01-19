from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings

from django.http import JsonResponse
from django.utils import timezone

from movies.models import Movie
from .models import Image_information, Tag, Photo
from .forms import PhotoForm

import random
import os, json, requests

from django.contrib.auth import get_user_model
User = get_user_model()



def index(request):
    return render(request, 'recommend/index.html')


# 좋아요 기반 추천 시스템
@login_required
def like(request):
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
        recommend_list = list(Movie.objects.filter(genres__pk=int(request.user.pick)))
    
    movies_top = random.choice(recommend_list)
    recommend_list.pop(recommend_list.index(movies_top))
    movies_top2 = random.sample(recommend_list, 2)

    context = {
        'movies_top' : movies_top,
        'movies_top2' : movies_top2,
    }
    
    return render(request, 'recommend/like.html', context)


@login_required
def photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.owner = request.user
            photo.pub_date = timezone.now()
            photo.save()
            return redirect('recommend:photo_recommend', photo.pk)
    else:
        form = PhotoForm()
    context = {
        'form': form,
    }
    return render(request, 'recommend/photo.html', context)



# 얼굴 표정 인식 기반 알고리즘 추천 시스템
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

NAVER_ID = get_secret('NAVER_ID')
NAVER_API_KEY = get_secret('NAVER_API_KEY')


@login_required
def photo_recommend(request, photo_pk):
    photo = get_object_or_404(Photo, pk=photo_pk)

    URL = "https://openapi.naver.com/v1/vision/face"
    files = { 'image': open(f'{photo.image.path}', 'rb')}
    headers = {'X-Naver-Client-Id': NAVER_ID, 'X-Naver-Client-Secret': NAVER_API_KEY }
    response = requests.post(URL, files=files, headers=headers)

    data = response.json()

    if data.get('faces'):
        emotion = data.get('faces')[0].get('emotion').get('value')
        if emotion == 'angry': # 화난
            recommend_list = Movie.objects.filter(genres__pk='28').filter(genres__pk='35')
            movies_top3 = random.sample(list(recommend_list), 3)
            movies_top = movies_top3[0]
            movies_top2 = movies_top3[1:]
        elif emotion == 'disgust': # 혐오감
            movies_top = '기분이 굉장히 안 좋은 것 같은데 오늘은 쉬시는게 어때요? :)'
            movies_top2 = []
        elif emotion == 'fear': # 두려움
            recommend_list = Movie.objects.filter(genres__pk='18').filter(genres__pk='10751')
            movies_top3 = random.sample(list(recommend_list), 3)
            movies_top = movies_top3[0]
            movies_top2 = movies_top3[1:]
        elif emotion == 'laugh': # 웃다
            recommend_list = Movie.objects.filter(genres__pk='14').filter(genres__pk='28').filter(genres__pk='878')
            movies_top3 = random.sample(list(recommend_list), 3)
            movies_top = movies_top3[0]
            movies_top2 = movies_top3[1:]
        elif emotion == 'neutral': # 중립
            recommend_list = Movie.objects.filter(genres__pk='53').filter(genres__pk='80')
            movies_top3 = random.sample(list(recommend_list), 3)
            movies_top = movies_top3[0]
            movies_top2 = movies_top3[1:]
        elif emotion == 'sad': # 서글
            recommend_list = Movie.objects.filter(genres__pk='10402').filter(genres__pk='10749')
            if len(recommend_list) < 3:
                recommend_list = []
                recommend_list.append(Movie.objects.filter(genres__pk='16'))
                recommend_list.append(Movie.objects.filter(genres__pk='10402'))
                recommend_list.append(Movie.objects.filter(genres__pk='10749'))
            movies_top3 = random.sample(list(recommend_list), 3)
            movies_top = movies_top3[0]
            movies_top2 = movies_top3[1:]
        elif emotion == 'surprise': # 깜짝놀람
            recommend_list = Movie.objects.filter(genres__pk='36').filter(genres__pk='99')
            if len(recommend_list) < 3:
                recommend_list = []
                recommend_list.append(Movie.objects.filter(genres__pk='36'))
                recommend_list.append(Movie.objects.filter(genres__pk='99'))
                recommend_list.append(Movie.objects.filter(genres__pk='10770'))
            movies_top3 = random.sample(list(recommend_list), 3)
            movies_top = movies_top3[0]
            movies_top2 = movies_top3[1:]
        elif emotion == 'smail': # 웃음
            recommend_list = Movie.objects.filter(genres__pk='12').filter(genres__pk='9648')
            movies_top3 = random.sample(list(recommend_list), 3)
            movies_top = movies_top3[0]
            movies_top2 = movies_top3[1:]
        else: # 말하는중
            recommend_list = Movie.objects.filter(genres__pk='27')
            movies_top3 = random.sample(list(recommend_list), 3)
            movies_top = movies_top3[0]
            movies_top2 = movies_top3[1:]
    else:
        movies_top = '얼굴이 나온 사진으로 올려주세요.'
        movies_top2 = []
        emotion = None

    context = {
        'photo': photo,
        'emotion': emotion,
        'movies_top' : movies_top,
        'movies_top2' : movies_top2,
    }

    return render(request, 'recommend/photo_recommend.html', context)