from django.shortcuts import render, redirect
from .models import Article, Editorial
from .forms import ArticleForm, EditorialForm

def home(request):
    art = Article.objects.all()
    return render(request,'base/home.html', {"article": art})

def get_article(request, slug):
    return render(request, 'articles/article.html',{"article":Article.objects.get(slug=slug)})

def article(request):
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            return redirect('/')
        else:
            message = "could not save form"
            return render(request, 'articles/article_form.html', {'message': message, 'form':form})
    else:
        return render(request, 'articles/article_form.html', {'form': form})