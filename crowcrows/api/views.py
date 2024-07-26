from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.http import Http404
from django.utils import timezone

from .auth import IsAdmin, IsEditor
from .serializer import (
    ArticleSerializer,
    UserSerializer,
    ArticleUpdateSerializer, ArticlePublishOrApproveSerializer,
)
from crowapp.mixins import ActivityLogMixin
from crowapp.models import (
    User,
    Author,
    Editor,
    Reader
)
from .auth import IsEditor, IsAdmin, IsAuthor, IsModerator
from blog.models import Article
from .utils import get_user_from_token


class ArticleListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        articles = Article.objects.filter(published_on__lte=timezone.now())
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


class ArticleCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [IsAuthor]

    def post(self, request):
        user = get_user_from_token(request.headers.get('Authorization', None))
        serializer = ArticleSerializer(data=request.data)
        if not user:
            return Response(
                data={status.HTTP_403_FORBIDDEN})
        if serializer.is_valid():
            serializer.save(created_by=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, exception=True)

    def patch(self, request):
        slug = request.query_params.get('q', None)
        article = Article.objects.get(slug=slug)
        if 'title' or 'content' in request.data:
            serializer = ArticleUpdateSerializer(article, data=request.data, partial=True)
        else:
            serializer = ArticlePublishOrApproveSerializer(article, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        article = Article.objects.get(slug=slug)
        ArticleSerializer(article, data={"hide": True})
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorArticleListView(APIView):
    authentication_classes = []
    permission_classes = [IsAuthenticated]

    def get(self, request):
        articles = Article.objects.filter(created_by=request.user)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):
    authentication_classes = []
    permission_classes = []

    def get_object(self, slug):
        try:
            return Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        article = self.get_object(slug)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status.HTTP_200_OK)


class UserListView(APIView):
    authentication_classes = [IsAdmin, IsModerator]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.filter(is_active=True)
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserDetailsView(APIView):
    authentication_classes = [IsAdmin, IsModerator]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self, pk):
        try:
            return Reader.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        if user.is_active:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        raise User.DoesNotExist

    def patch(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorListView(APIView):
    authentication_classes = [IsAdmin, IsModerator]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = Author.objects.filter(active=True)
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorDetailsView(APIView):
    authentication_classes = [IsAdmin, IsModerator, IsEditor]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        UserSerializer(user, {"is_active": False})
        return Response(status=status.HTTP_204_NO_CONTENT)


class EditorListView(APIView):
    authentication_classes = [IsAdmin, IsModerator]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = Editor.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditorDetailsView(APIView):
    authentication_classes = [IsAdmin, IsModerator, IsEditor]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Editor.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        UserSerializer(user, {"is_active": False})
        return Response(status=status.HTTP_204_NO_CONTENT)


# class ArticleRListView(ActivityLogMixin, APIView):
#     def get(self, request, *args, **kwargs):
#         return Response({"articles": Article.objects.values()})

class PostReadOnlyViewSet(ActivityLogMixin, ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_log_message(self, request) -> str:
        return f"{request.user} is reading blog posts"


class StatsView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        filter_params = request.query_params.get('filter', 'all')

        now = timezone.now()

        filter_mapping = {
            'daily': Q(published_on__date=now.date()),
            'weekly': Q(published_on__week=now.isocalendar()[1], published_on__year=now.year),
            'monthly': Q(published_on__month=now.month, published_on__year=now.year),
            'all': Q()
        }

        filter_query = filter_mapping.get(filter_params, Q())
        queryset = Article.objects.filter(filter_query)

        published_articles = queryset.filter(published=True)
        scheduled_articles = Article.objects.filter(published_on__gt=now)
        all_articles = Article.objects.exclude(published_on=None)
        all_authors = all_articles.values('created_by').distinct()

        data = {
            'total_articles': all_articles.count(),
            'published_articles': published_articles.count(),
            'scheduled_articles': scheduled_articles.count(),
            'total_authors': all_authors.count()
        }

        return Response(data)