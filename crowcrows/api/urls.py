from django.urls import path, include

from .views import (
    ArticleList,
    ArticleDetail
)

urlpatterns = [
    path('articles/', ArticleList.as_view()),
    path('article/<int:id>', ArticleDetail.as_view()),
]