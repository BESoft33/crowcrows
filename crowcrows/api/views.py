from urllib import request
from django.shortcuts import render

from rest_framework.decorators import (
    api_view, 
)
from rest_framework.response import Response

from .serializer import (
    ArticleSerializer,
    BloggerSerializer,
)

from crowapp.models import (
    Article,
    User,
)

@api_view(['GET'])
def api_overviev(request):
    api_urls = {
        'article_detail':'detail/<str:slug>/',
        'article_list':'articles/',
        'update_article':'',  
        'delete_article':'article/<str:slug>/',
    }
    return Response(api_urls)

@api_view(['GET'])
def all_articles(request):
    articles = Article.objects.all()

    serializer = ArticleSerializer(articles, many=True)

    return Response(serializer.data)