from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('message/', views.list_msg, name='list_msg'),
    path('message/send/<int:user_pk>/', views.send_msg, name='send_msg'),
    path('message/<int:message_pk>/delete/', views.delete_msg, name='delete_msg'),
]