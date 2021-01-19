from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from movies.models import Movie
from movies.models import Genre, Movie

from faker import Faker

f = Faker()

class User(AbstractUser):
    pick_genre = (
        ('12', '모험'),
        ('14', '판타지'),
        ('16', '애니메이션'),
        ('18', '드라마'),
        ('27', '공포'),
        ('28', '액션'),
        ('35', '코미디'),
        ('36', '역사'),
        ('37', '서부'),
        ('53', '스릴러'),
        ('80', '범죄'),
        ('99', '다큐멘터리'),
        ('878', 'SF'),
        ('9648', '미스터리'),
        ('10402', '음악'),
        ('10749', '로맨스'),
        ('10751', '가족'),
        ('10752', '전쟁'),
        ('10770', 'TV 영화')
    )
    pick = models.CharField(
        max_length=5,
        choices=pick_genre,
    )
    like_genres = models.ManyToManyField(Genre, related_name="user_like", blank=True)


    @classmethod
    def dummy(cls, n):
        for _ in range(n):
            genre = Genre.objects.order_by('?')[0]
            username = f.simple_profile().get('username')
            cls.objects.create(
                username = username,
                first_name = f.first_name(),
                last_name = f.last_name(),
                password = f.password(length=8),
                pick = str(genre.pk),
            )



class Message(models.Model):
    send_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="msg_send_user", on_delete=models.CASCADE)
    receive_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="msg_receive_user", on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=150)

    # 디폴트 모델 매니저
    objects = models.Manager()

    def save(self, **kwargs):
        if not self.id:
            self.sent_at = timezone.now()
        super(Message, self).save(**kwargs)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return self.content