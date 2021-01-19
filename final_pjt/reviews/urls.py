from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.index, name='index'),
    path('search_review/', views.search_review, name='search_review'),
    path('movie_search/', views.movie_search, name='movie_search'),
    path('movie_search_modal/', views.movie_search_modal, name='movie_search_modal'),
    path('create_review/<int:movie_pk>/', views.create_review, name='create_review'),
    path('<int:review_pk>/', views.detail_review, name='detail_review'),
    path('<int:review_pk>/like/', views.like, name='like'),
    path('<int:review_pk>/update/', views.update_review, name='update_review'),
    path('<int:review_pk>/delete/', views.delete_review, name='delete_review'),
    path('<int:review_pk>/comments/', views.create_comment, name='create_comment'),
    path('<int:review_pk>/comments/<int:comment_pk>/delete/', views.delete_comment, name='delete_comment'),
]