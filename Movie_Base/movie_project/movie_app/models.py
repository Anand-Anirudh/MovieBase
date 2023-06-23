from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', null=True, blank=True, on_delete=models.CASCADE)
    tv = models.ForeignKey('TV', null=True, blank=True, on_delete=models.CASCADE)
    comment = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    profile_info = models.TextField(max_length=150, null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    picture=CloudinaryField('image')
    def __str__(self):
        return self.user.username
        

class Genre(models.Model):
    genre_id = models.IntegerField()
    name = models.CharField(max_length=100)
    movie = models.ForeignKey('Movie', null=True, blank=True,on_delete=models.CASCADE,related_name='genre')
    tv = models.ForeignKey('TV', null=True, blank=True,on_delete=models.CASCADE,related_name='genre_tv')

    def __str__(self):
        return self.name
    
class Cast(models.Model):
    name = models.CharField(max_length=255)
    character = models.CharField(max_length=255)
    profile_path = models.CharField(max_length=255, blank=True, null=True)
    movie = models.ForeignKey('Movie', null=True, blank=True, on_delete=models.CASCADE,related_name='cast_members')
    tv = models.ForeignKey('TV', null=True, blank=True, on_delete=models.CASCADE,related_name='cast_members')

    def __str__(self):
        return self.name

    
    
class Movie(models.Model):
    movie_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    overview = models.TextField()
    status= models.CharField(max_length=30)
    release_date = models.CharField(max_length=40)
    popularity = models.FloatField()
    poster_path = models.CharField(max_length=200)
    runtime = models.IntegerField(null=True, blank=True)
    tagline = models.CharField(max_length=200, null=True, blank=True)
    budget = models.IntegerField()
    revenue=models.IntegerField()
    vote_average= models.FloatField()
    vote_count= models.IntegerField()
    genres = models.ManyToManyField(Genre,related_name='movies_genre')
    cast = models.ManyToManyField(Cast, related_name='movies_cast')
    reviews = models.ManyToManyField(Review, related_name='movies', blank=True)
    
    def __str__(self):
        return self.title
    
class TV(models.Model):
    tv_series_id= models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    overview = models.TextField()
    first_air_date= models.CharField(max_length=40)
    last_air_date = models.CharField(max_length=40)
    status = models.CharField(max_length=100)
    popularity=models.FloatField()
    poster_path=models.CharField(max_length=200)
    number_of_seasons = models.IntegerField()
    number_of_episodes = models.IntegerField()
    vote_average= models.FloatField()
    vote_count= models.IntegerField()
    genres = models.ManyToManyField(Genre,related_name='tv_genre')
    cast = models.ManyToManyField(Cast, related_name='tv_series_cast')
    reviews = models.ManyToManyField(Review, related_name='tv_series', blank=True)
   
    def __str__(self):
        return self.title
