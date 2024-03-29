from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home),
    path('article/new/', views.article, name='new_article'),
    path('article/<str:slug>', views.article, name='article'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),  
    path('logout/',views.logout_view, name='logout')

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
