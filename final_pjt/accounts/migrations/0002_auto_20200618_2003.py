# Generated by Django 2.1.15 on 2020-06-18 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('movies', '0001_initial'),
        ('auth', '0009_alter_user_last_name_max_length'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='like_genres',
            field=models.ManyToManyField(blank=True, related_name='user_like', to='movies.Genre'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
