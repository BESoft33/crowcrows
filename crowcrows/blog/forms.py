from django import forms
from .models import Article, Editorial
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Article
        fields = ("title", "published_on", "content")
        widgets = {

        }


class EditorialForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Editorial
        fields = ("title", "published_on", "content")
        widgets = {

        }