from django.shortcuts import render,redirect
import requests
from .tmdb import search_movies
from .models import Movie,Genre,TV,Cast,Profile
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import  login,logout,authenticate
from django.contrib import messages
from django.contrib.auth .decorators import login_required
from .forms import ProfileForm


# Create your views here.
api_key="a0e658d14540c501d60bf848cbab3db0"

def new(request):
    return render(request,"new.html")


def signup(request):
    if  request.method == 'GET':
        return render (request,'signup.html')
    else:
        username = request.POST['Username']
        email = request.POST['Email']
        password = request.POST['Password']
        confirmPassword = request.POST['ConfirmPassword']

        if password == confirmPassword:
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username Alreaady Exists')
                return redirect('signup')
            
            elif User.objects.filter(email=email).exists():
                messages.error(request,'Email Alreaady Exists')
                return redirect('signup')
            
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return redirect('signin')
        else:
            messages.error(request,'Try Matching Password')
            return redirect('signup')

def signin(request):
    if  request.method == 'GET':
        return render (request,'login.html')
    else:
        username = request.POST['Username']
        password = request.POST['Password']

        user = authenticate(username=username,password=password)

        if user is None:
            messages.error(request,'Invalid Username / Password')
            return redirect('signin')
        else:
            login(request,user)
            return redirect('profile')

def UserLogout(request):
    logout(request)
    return redirect('index')

@login_required(login_url='signin')
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        if 'first_name' in request.POST:
            profile.first_name = request.POST['first_name']
        if 'last_name' in request.POST:
            profile.last_name = request.POST['last_name']
        if 'location' in request.POST:
            profile.location = request.POST['location']
        if 'profile_info' in request.POST:
            profile.profile_info = request.POST['profile_info']
        if 'picture' in request.FILES:
            profile.picture = request.FILES['picture']
        profile.save()
        return redirect('profile')
    
    context = {'profile': profile}
    return render(request, 'profile.html', context)

def movie_catalog(request):
    genre_id = request.GET.get('genre_id')
    page_number = request.GET.get('page', 1)
    
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre_id}'
    response = requests.get(url)
    data = response.json()
    movies = data.get('results', [])

    # Create a Paginator object with the movies list and desired number of movies per page
    movies_per_page = 10  # Adjust this value as per your requirement
    paginator = Paginator(movies, movies_per_page)

    # Get the requested page
    page = paginator.get_page(page_number)

    return render(request, 'catalog.html', {'page': page})


def index(request):
    return render(request,"index.html")

def  search(request):
    query= request.GET.get('q')
    
    if query:
        results = search_movies(query, api_key)
    else:
        results = []
    paginator = Paginator(results, 8)  # Display 10 results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'query': query,
        'results': page_obj,
    }
    return render(request,'search.html', context)
@login_required(login_url='signin')
def movie_details(request, movie_id):
    
    
    videos_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={api_key}"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}"
    response = requests.get(url)
    videos_response = requests.get(videos_url)
    credits_response = requests.get(credits_url)
    movie_data = response.json()
    videos_data = videos_response.json()
    credits_data = credits_response.json()
    trailer_key = None
    if 'results' in videos_data:
        results = videos_data['results']
        for result in results:
            if result.get('type') == 'Trailer' and result.get('site') == 'YouTube':
                trailer_key = result.get('key')
                break



    if Movie.objects.filter(movie_id=movie_id).exists():
        movie = Movie.objects.get(movie_id=movie_id)
        our_db = True
    else:
        # Create a new movie object in your database
        movie, created = Movie.objects.get_or_create(
            movie_id=movie_id,
            title=movie_data['title'],
            overview=movie_data['overview'],
            status= movie_data['status'],
            release_date=movie_data['release_date'],
            popularity=movie_data['popularity'],
            poster_path=movie_data['poster_path'],
            runtime=movie_data['runtime'],
            tagline=movie_data['tagline'],
            budget = movie_data['budget'],
            revenue=movie_data['revenue'],
            vote_average= movie_data['vote_average'],
            vote_count= movie_data['vote_count'],
            
            
            # Add other relevant fields based on the API response
        )

        genre=[]
        genres_data = movie_data['genres']
        for genre_data in genres_data:
            genre_obj, _ = Genre.objects.get_or_create(
                genre_id=genre_data['id'],
                name= genre_data['name'],
                movie=movie
            )
            genre.append(genre_obj)
            movie.genres.add(genre_obj)
        


    cast=[]
    if 'cast' in credits_data:
        cast_data = credits_data['cast']
        for cast_member in cast_data[:8]:  # Limiting to 10 cast members for display
            cast_obj, _ = Cast.objects.get_or_create(
                name=cast_member['name'],
                character=cast_member['character'],
                profile_path=cast_member['profile_path'],
                movie=movie
            )
            cast.append(cast_obj)
            movie.cast.add(cast_obj)

    if request.method == 'POST':
        comment = request.POST['comment']
        user = request.user
        movie.reviews.create(user=user, comment=comment,movie=movie)
        return redirect('movie_details', movie_id=movie_id)
        
        

    our_db=False   
    
    context = {
        'movie_data': movie_data,
        'trailer_key': trailer_key,
        'our_db': our_db,
        'movie': movie,
        'cast': cast,
        'reviews': movie.reviews.all(),
        
        
        
    }
    return render(request, 'movie_details.html', context)
@login_required(login_url='signin')
def tv_series_details(request, tv_series_id):
    
    
    videos_url = f"https://api.themoviedb.org/3/tv/{tv_series_id}/videos?api_key={api_key}"
    url = f"https://api.themoviedb.org/3/tv/{tv_series_id}?api_key={api_key}"
    credits_url = f"https://api.themoviedb.org/3/tv/{tv_series_id}/credits?api_key={api_key}"
    response = requests.get(url)
    videos_response = requests.get(videos_url)
    credits_response = requests.get(credits_url)
    tv_series_details = response.json()
    videos_data = videos_response.json()
    credits_data = credits_response.json()
    trailer_key = None
    if 'results' in videos_data:
        results = videos_data['results']
        for result in results:
            if result.get('type') == 'Trailer' and result.get('site') == 'YouTube':
                trailer_key = result.get('key')
                break



    if TV.objects.filter(tv_series_id=tv_series_id).exists():
        tv = TV.objects.get(tv_series_id=tv_series_id)
        our_db = True
    else:
        # Create a new movie object in your database
        tv, created = TV.objects.get_or_create(
            tv_series_id=tv_series_id,
            title=tv_series_details['name'],
            overview=tv_series_details['overview'],
            first_air_date=tv_series_details['first_air_date'],
            last_air_date=tv_series_details['last_air_date'],
            status= tv_series_details['status'],
            popularity=tv_series_details['popularity'],
            poster_path=tv_series_details['poster_path'],
            number_of_seasons=tv_series_details['number_of_seasons'],
            number_of_episodes=tv_series_details['number_of_episodes'],
            vote_average=tv_series_details['vote_average'],
            vote_count=tv_series_details['vote_count'],
            
            
            
            # Add other relevant fields based on the API response
        )

        genre=[]
        genres_data = tv_series_details['genres']
        for genre_data in genres_data:
            genre_obj, _ = Genre.objects.get_or_create(
                genre_id=genre_data['id'],
                name= genre_data['name'],
                tv=tv
            )
            genre.append(genre_obj)
            tv.genres.add(genre_obj)

    cast=[]
    if 'cast' in credits_data:
        cast_data = credits_data['cast']
        for cast_member in cast_data[:8]:  # Limiting to 10 cast members for display
            cast_obj, _ = Cast.objects.get_or_create(
                name=cast_member['name'],
                character=cast_member['character'],
                profile_path=cast_member['profile_path'],
                tv=tv
            )
            cast.append(cast_obj)
            tv.cast.add(cast_obj)
           
    if request.method == 'POST':
        comment = request.POST['comment']
        user = request.user
        tv.reviews.create(user=user, comment=comment)
        return redirect('tv_series_details', tv_series_id=tv_series_id)  
        

    our_db=False   
    
    context = {
        'tv_series_details': tv_series_details,
        'trailer_key': trailer_key,
        'our_db': our_db,
        'tv': tv,
        'cast': cast,
        'reviews': tv.reviews.all(),
        
        
        
        
    }
    return render(request, 'tv_series_details.html', context)


def movies(request):
    genre_id = request.GET.get('genre_id')
    page_number = request.GET.get('page', 1)
    
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre_id}'
    response = requests.get(url)
    data = response.json()
    movies = data.get('results', [])

    # Create a Paginator object with the movies list and desired number of movies per page
    movies_per_page = 8  # Adjust this value as per your requirement
    paginator = Paginator(movies, movies_per_page)

    # Get the requested page
    page = paginator.get_page(page_number)

    return render(request, 'movies.html', {'page': page})



def tv_series(request):
    
    genre_id = request.GET.get('genre_id')
    page_number = request.GET.get('page', 1)
    
    url = f'https://api.themoviedb.org/3/discover/tv?api_key={api_key}&with_genres={genre_id}'
    response = requests.get(url)
    data = response.json()
    tv_series = data.get('results', [])

    # Create a Paginator object with the movies list and desired number of movies per page
    tv_series_per_page = 8  # Adjust this value as per your requirement
    paginator = Paginator(tv_series, tv_series_per_page)

    # Get the requested page
    page = paginator.get_page(page_number)

    return render(request, 'tv_series.html', {'page': page})











