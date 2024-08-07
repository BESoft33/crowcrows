from django.db.models import Q, Count
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.http import Http404
from django.utils import timezone

from .auth import IsAdmin, IsEditor
from .serializer import (
    ArticleSerializer,
    UserSerializer,
    ArticleUpdateSerializer, ArticlePublishOrApproveSerializer, StatisticsSerializer,
)
from users.mixins import ActivityLogMixin
from users.models import (
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


class ArticleView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [IsAuthor, IsAdmin]

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, exception=True)

    def patch(self, request):
        slug = request.query_params.get('q', None)
        article = Article.objects.get(slug=slug)
        serializer = ArticleUpdateSerializer(article, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        article = Article.objects.get(slug=slug)
        ArticleSerializer(article, data={"hide": True})
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorArticleListView(APIView):
    authentication_classes = [IsAuthor, IsAdmin]
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
    permission_classes = [AllowAny]

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
    authentication_classes = [IsAdmin, IsModerator]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()

        today_published = Count("id", filter=Q(published_on__date=now.date()))
        this_month_published = Count("id", filter=Q(published_on__month=now.month, published_on__year=now.year))
        this_year_published = Count("id", filter=Q(published_on__year=now.year))
        total_published = Count("id", filter=Q(published=True, published_on__lte=now))
        total_scheduled = Count("id", filter=Q(published=True, published_on__gt=now, approved_by__isnull=False))
        asking_approval = Count("id", filter=Q(approved_by__isnull=False, published=True, published_on__gt=now))
        total_unapproved = Count("id", filter=Q(approved_by__isnull=True, published=True, published_on__lte=now))

        article_stats = Article.objects.aggregate(
            total_articles=Count("id"),
            total_published=total_published,
            total_scheduled=total_scheduled,
            asking_approval=asking_approval,
            total_approved=total_published,
            total_unapproved=total_unapproved,
            today_published=today_published,
            this_month_published=this_month_published,
            this_year_published=this_year_published,
        )

        active_authors_count = Author.objects.filter(is_active=True).count()
        active_readers_count = Reader.objects.filter(is_active=True).count()

        data = {
            "article": {
                "total_articles": article_stats["total_articles"],
                "total_published": article_stats["total_published"],
                "total_scheduled": article_stats["total_scheduled"],
                "asking_approval": article_stats["asking_approval"],
                "total_approved": article_stats["total_approved"],
                "total_unapproved": article_stats["total_unapproved"],
                "today_published": article_stats["today_published"],
                "this_month_published": article_stats["this_month_published"],
                "this_year_published": article_stats["this_year_published"],
            },
            "user_stats": {
                "active_authors": active_authors_count,
                "active_readers": active_readers_count,
            }
        }

        serializer = StatisticsSerializer(data)
        return Response(serializer.data)