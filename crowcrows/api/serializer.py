from rest_framework import serializers

from  crowapp.models import(
    Blogger,
    Article, 
)
class BloggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogger
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
