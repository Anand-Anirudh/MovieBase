"""movie_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from movie_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",views.index,name='index'),
    path("search",views.search,name='search'),
    path('movie/<int:movie_id>/', views.movie_details, name='movie_details'),
    path('tv-series/<int:tv_series_id>/', views.tv_series_details, name='tv_series_details'),
    path('movies/', views.movies, name='movies'),
    path('tv_series/', views.tv_series, name='tv_series'),
    path('signup',views.signup,name='signup'),
    path('signin',views.signin, name='signin'),
    path("logout/",views.UserLogout,name='logout'),
    path('profile',views.profile, name='profile'),
    path("new",views.new),
    
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
