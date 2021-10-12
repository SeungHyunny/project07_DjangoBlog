from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import mysite.views
from mysite.views import HomeView, BotView
from mysite.views import UserCreateView, UserCreateDoneTV


urlpatterns = [
    # path('',views.start),
    path('admin/', admin.site.urls),
    path('',HomeView.as_view(),name='home'),
    path('bookmark/',include('bookmark.urls')),
    path('blog/',include('blog.urls')),
    path('polls/',include('polls.urls')),
    path('photo/',include('photo.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/register/',UserCreateView.as_view(),name='register'),
    path('accounts/register/done/',UserCreateDoneTV.as_view(),name='register_done'),
    path('chatbot/', BotView.as_view(), name='chatbot'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
