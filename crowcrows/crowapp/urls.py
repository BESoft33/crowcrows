from django.urls import path
from . import views
import blog

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),  
    path('logout/',views.logout_view, name='logout')

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
