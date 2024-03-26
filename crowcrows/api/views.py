from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404

from .serializer import (
    ArticleSerializer,
    BloggerSerializer,
)

from crowapp.models import (
    Article,
    User,
)

class ArticleList(APIView):
    permission_classes = []

    def get(self, request):
        articles = Article.objects.filter(published=True)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        title = request.POST.get('title')
        content = request.POST.get('content')
        created_by = request.user

        article = Article.objects.create(title=title, content=content, created_by=created_by)
        if article:
            return Response({"message": "Article created successfully!"})
        return Response({"message": "Could not create article!"})
    
class ArticleDetail(APIView):
    permission_classes = []

    def get_object(self, id):
        try:
            return Article.objects.get(id=id)
        except Article.DoesNotExist:
            raise Http404    
        
    def get(self, request, id):
        article = self.get_object(id=id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, id):
        article = self.get_object(id=id)

        serializer = ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        article = self.get_object(id=id)
        serializer = ArticleSerializer(article, data=article)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)