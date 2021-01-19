from django.db import models
from django.conf import settings
import os, json, requests


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

API_KEY = get_secret('API_KEY')



class Genre(models.Model):
    name = models.CharField(max_length=100)

    @classmethod
    def get_genres(cls):
        GENRE_URL = f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=ko-KR"
        genredata = requests.get(GENRE_URL)
        genres = genredata.json().get('genres')

        for genre in genres:
            cls.objects.create(
                pk = genre.get('id'),
                name = genre.get('name')
            )



class Movie(models.Model):
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_average = models.FloatField()
    adult = models.BooleanField()
    overview = models.TextField()
    original_language = models.CharField(max_length=50)
    poster_path = models.CharField(max_length=300, blank=True)
    backdrop_path = models.CharField(max_length=300, blank=True)
    genres = models.ManyToManyField(Genre)
    homepage = models.CharField(max_length=300, blank=True)
    tagline = models.TextField()
    runtime = models.IntegerField()
    status = models.CharField(max_length=50)
    director = models.CharField(max_length=100)
    production_countrie = models.CharField(max_length=50)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_movies", blank=True)

    @classmethod
    def get_movies(cls):

        for page in range(1,30):

            URL = f'https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&language=ko-KR&page={page}'
            movie_data = requests.get(URL)
            datas = movie_data.json().get('results')

            for data in datas:
                if not data.get('release_date'):
                    continue

                # detail 에서 데이터 찾기
                detail_URL = f"https://api.themoviedb.org/3/movie/{data.get('id')}?api_key={API_KEY}&language=ko-KR"
                detail_data = requests.get(detail_URL).json()

                if detail_data.get('homepage') != None:
                    homepage = detail_data.get('homepage')
                else:
                    homepage = ''
                
                if len(detail_data.get('production_countries')) > 0:
                    production_countrie = detail_data.get('production_countries')[0].get('iso_3166_1')
                else:
                    production_countrie = ''

                tagline = detail_data.get('tagline')

                if not type(detail_data.get('runtime')) != int:
                    runtime = detail_data.get('runtime')
                else:
                    runtime = 0

                status = detail_data.get('status')



                # credit 에서 데이터 찾기
                credit_URL = f"https://api.themoviedb.org/3/movie/{data.get('id')}/credits?api_key={API_KEY}"

                crew_datas = requests.get(credit_URL).json().get('crew')
                for crew_data in crew_datas:
                    if crew_data.get('job') == 'Director':
                        director = crew_data.get('name')
                        break
                


                if not data.get('poster_path'):
                    continue
                else:
                    data['poster_path'] = 'https://image.tmdb.org/t/p/original' + data['poster_path']

                if not data.get('backdrop_path'):
                    continue
                else:
                    data['backdrop_path'] = 'https://image.tmdb.org/t/p/original' + data['backdrop_path']




                cls.objects.create(
                    pk = data.get('id'),
                    title = data.get('title'),
                    release_date = data.get('release_date'),
                    original_title = data.get('original_title'),
                    popularity = data.get('popularity'),
                    vote_average = data.get('vote_average'),
                    adult = data.get('adult'),
                    overview = data.get('overview'),
                    original_language = data.get('original_language'),
                    poster_path = data.get('poster_path'),
                    backdrop_path = data.get('backdrop_path'),
                    homepage = homepage,
                    production_countrie = production_countrie,
                    tagline = tagline,
                    runtime = runtime,
                    status = status,
                    director = director,
                )

                new_movie = cls.objects.get(pk=data.get('id'))
                temp_genres = []
                for genre_id in data.get('genre_ids'):
                    genre = Genre.objects.get(pk=genre_id)
                    temp_genres.append(genre)
                new_movie.genres.set(temp_genres)