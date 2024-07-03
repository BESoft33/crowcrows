from rest_framework import serializers
from crowapp.models import (
    User,
)
from blog.models import Article


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password',]


class ArticleSerializer(serializers.ModelSerializer):
    created_by = UserSerializer( read_only=True)
    class Meta:
        model = Article
        fields = '__all__'
