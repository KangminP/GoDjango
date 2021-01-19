from django.contrib import admin
from .models import Photo, Image_information, Tag

# Register your models here.
admin.site.register(Photo)
admin.site.register(Image_information)
admin.site.register(Tag)