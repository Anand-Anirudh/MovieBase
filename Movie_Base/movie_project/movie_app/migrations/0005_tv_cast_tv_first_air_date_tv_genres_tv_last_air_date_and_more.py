# Generated by Django 4.1.7 on 2023-06-02 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movie_app", "0004_remove_tv_cast_remove_tv_first_air_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tv",
            name="cast",
            field=models.ManyToManyField(
                related_name="tv_series_cast", to="movie_app.cast"
            ),
        ),
        migrations.AddField(
            model_name="tv",
            name="first_air_date",
            field=models.CharField(default=2, max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tv",
            name="genres",
            field=models.ManyToManyField(related_name="tv_genre", to="movie_app.genre"),
        ),
        migrations.AddField(
            model_name="tv",
            name="last_air_date",
            field=models.CharField(default=2, max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tv",
            name="number_of_episodes",
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tv",
            name="number_of_seasons",
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tv",
            name="overview",
            field=models.TextField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tv",
            name="popularity",
            field=models.FloatField(default=21),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tv",
            name="poster_path",
            field=models.CharField(default=2, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tv",
            name="status",
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tv",
            name="vote_average",
            field=models.FloatField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tv",
            name="vote_count",
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]