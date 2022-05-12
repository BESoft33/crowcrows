from django.db import models
# from froala_editor.fields import FroalaField
# from tinymce.models import HTMLField
from ckeditor.fields import RichTextField





class Blogger(models.Model):
    first_name = models.CharField(max_length=20, blank= False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null= False)
    photo = models.ImageField()

    def __str__(self):
        return self.first_name

class Article(models.Model):
    title = models.CharField(max_length=128, default='')
    published_on = models.DateTimeField(auto_now_add=True)
    content = RichTextField()
    image = models.ImageField(upload_to='images',blank=True, null=True)

    hide = models.BooleanField(default=False)
    slug = models.SlugField(max_length=128, unique=True, blank=True, null=True)
    blogger = models.ForeignKey(to=Blogger, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title 



# class Controller(models.Model):
#     pass
