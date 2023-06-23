from django.contrib import admin
from .models import Genre,Movie,TV,Cast,Review,Profile

# Register your models here.
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Cast)
admin.site.register(Review)
admin.site.register(TV)
admin.site.register(Profile)


