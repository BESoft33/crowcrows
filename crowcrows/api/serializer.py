from rest_framework import serializers
from crowapp.models import (
    User,
)
from blog.models import Article


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional fields argument
    that returns specified fields
    """

    def __init__(self, *args, **kwargs):
        # Remove the fields args before passing into the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass without fields argument
        super().__init__(*args, **kwargs)

        if fields:
            allowed_fields = set(fields)
            all_fields = set(self.fields)

            for field in all_fields - allowed_fields:
                # Remove the fields that are not in allowed_fields
                self.fields.pop(field)


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
        }


class ArticleSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True, fields=('id', 'first_name', 'last_name', 'profile_img'))

    class Meta:
        model = Article
        fields = '__all__'
