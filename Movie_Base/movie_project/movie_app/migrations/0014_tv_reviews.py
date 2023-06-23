# Generated by Django 4.1.7 on 2023-06-12 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movie_app", "0013_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="tv",
            name="reviews",
            field=models.ManyToManyField(
                blank=True, related_name="tv_series", to="movie_app.review"
            ),
        ),
    ]
