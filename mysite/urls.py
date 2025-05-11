from django.contrib import admin
from django.urls import path, include
from anilist import views


urlpatterns = [
    path('page/', include('anilist.urls')),
    path('admin/', admin.site.urls),
]
