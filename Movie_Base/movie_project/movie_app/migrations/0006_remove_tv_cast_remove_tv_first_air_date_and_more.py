# Generated by Django 4.1.7 on 2023-06-02 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "movie_app",
            "0005_tv_cast_tv_first_air_date_tv_genres_tv_last_air_date_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tv",
            name="cast",
        ),
        migrations.RemoveField(
            model_name="tv",
            name="first_air_date",
        ),
        migrations.RemoveField(
            model_name="tv",
            name="genres",
        ),
        migrations.RemoveField(
            model_name="tv",
            name="last_air_date",
        ),
        migrations.RemoveField(
            model_name="tv",
            name="number_of_episodes",
        ),
        migrations.RemoveField(
            model_name="tv",
            name="number_of_seasons",
        ),
        migrations.RemoveField(
            model_name="tv",
            name="popularity",
        ),
        migrations.RemoveField(
            model_name="tv",
            name="poster_path",
        ),
        migrations.RemoveField(
            model_name="tv",
            name="vote_average",
        ),
        migrations.RemoveField(
            model_name="tv",
            name="vote_count",
        ),
    ]
