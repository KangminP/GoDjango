from django.urls import path
from . import views

app_name = 'recommend'

urlpatterns = [
    path('', views.index, name='index'),
    path('like/', views.like, name='like'),
    path('photo/', views.photo, name='photo'),
    path('photo/<int:photo_pk>/', views.photo_recommend, name='photo_recommend'),
]
