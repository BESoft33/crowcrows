from rest_framework import serializers
from crowapp.models import (
    User,
    Article,
)


class BloggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
