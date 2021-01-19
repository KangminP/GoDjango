from django.db import models
from django.conf import settings

from faker import Faker

from movies.models import Movie

from django.contrib.auth import get_user_model
User = get_user_model()

f = Faker()

class Review(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    review_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='review_movie', on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_reviews", blank=True)

    @classmethod
    def dummy(cls, n):
        for _ in range(n):
            user = User.objects.order_by('?')[0]
            movie = Movie.objects.order_by('?')[0]
            cls.objects.create(
                title = f.sentence(),
                content = f.text(),
                review_user = user,
                movie = movie,
            )

class Comment(models.Model):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)