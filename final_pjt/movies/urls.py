from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('<int:movie_pk>/', views.movie_detail, name='movie_detail'),
    path('<int:movie_pk>/related', views.related_reviews, name='related_reviews'),
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('latest/', views.latest, name='latest'),
    path('ranked/', views.ranked, name='ranked'),
    path('popular/', views.popular, name='popular'),
]
