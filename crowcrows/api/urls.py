from django.urls import path, include

from .views import *

urlpatterns = [
    path('',api_overviev, name="overview"),
    path('articles/', all_articles)
]