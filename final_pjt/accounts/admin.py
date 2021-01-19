from django.contrib import admin
from .models import User
from .models import Message


# Register your models here.
admin.site.register(User)
admin.site.register(Message)
