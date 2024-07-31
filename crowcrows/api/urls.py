from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    ArticleListView,
    ArticleDetailView,
    UserListView,
    UserDetailsView,
    AuthorListView,
    AuthorDetailsView,
    EditorListView,
    EditorDetailsView,
    ArticleView,
    StatsView, AuthorArticleListView
)

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('article/', ArticleView.as_view(), name='article-create'),
    path('article/<str:slug>/', ArticleDetailView.as_view(), name='article'),
    path('users/', UserListView.as_view(), name='users'),
    path('user/<int:pk>/', UserDetailsView.as_view(), name='user'),
    path('author/articles/', AuthorArticleListView.as_view(), name='author-articles'),
    path('authors/', AuthorListView.as_view(), name='users'),
    path('author/<int:pk>/', AuthorDetailsView.as_view(), name='user'),
    path('editors/', EditorListView.as_view(), name='users'),
    path('editor/<int:pk>/', EditorDetailsView.as_view(), name='user'),
    path('stats/', StatsView.as_view(), name='stats'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
