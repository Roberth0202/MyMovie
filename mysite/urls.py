from django.contrib import admin
from django.urls import path, include
from mymovie import views


urlpatterns = [
    path('', include('mymovie.urls')),
    path('admin/', admin.site.urls),
]
