from django.db import models
from django.conf import settings
import os, json, requests

from movies.models import Movie


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

KAKAO_API_KEY = get_secret('KAKAO_API_KEY')


class Tag(models.Model):
    label = models.CharField(max_length=100)


class Image_information(models.Model):
    tag = models.ManyToManyField(Tag, blank=True)

    @classmethod
    def get_image_informations(cls):
        movies = Movie.objects.all()
        headers = {'Authorization': 'KakaoAK {}'.format(KAKAO_API_KEY)}

        for movie in movies:
            data = { 'image_url' : f'{movie.backdrop_path}'}

            TAG_URL = 'https://kapi.kakao.com/v1/vision/multitag/generate'
            tag_datas = requests.post(TAG_URL, headers=headers, data=data)

            tags = []
            try:
                if tag_datas.json().get('result').get('label_kr'):
                    for tag in tag_datas.json().get('result').get('label_kr'):
                        if Tag.objects.filter(label = tag):
                            tags += Tag.objects.filter(label = tag)
                        else:
                            tags.append(Tag.objects.create(label = tag))
            except:
                continue

            cls.objects.create(
                pk = movie.pk,
            )

            new_img_info = cls.objects.get(pk=movie.pk)
            new_img_info.tag.set(tags)


def user_path(instance, filename): #파라미터 instance는 Photo 모델을 의미 filename은 업로드 된 파일의 파일 이름
    from random import choice
    import string # string.ascii_letters : ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr) # 8자리 임의의 문자를 만들어 파일명으로 지정
    extension = filename.split('.')[-1] # 배열로 만들어 마지막 요소를 추출하여 파일확장자로 지정
    # file will be uploaded to MEDIA_ROOT/user_<id>/<random>
    return f'{instance.owner.username}/{pid}.{extension}' # 예 : wayhome/abcdefgs.png

class Photo(models.Model):
    image = models.ImageField(upload_to = user_path) # 어디로 업로드 할지 지정
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 로그인 한 사용자, many to one relation
    thumname_image = models.ImageField(blank = True) # 필수입력 해제
    pub_date = models.DateTimeField(auto_now_add = True) # 레코드 생성시 현재 시간으로 자동 생성