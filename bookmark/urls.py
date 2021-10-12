from django.urls import path
from bookmark.views import BookmarkLV,BookmarkDV
from bookmark import views

app_name = 'bookmark' #네임스페이스

urlpatterns = [
    path('', BookmarkLV.as_view(), name='index'),
    
    path('<int:pk>/', BookmarkDV.as_view(), name='detail'),

    path('add/', views.BookmarkCreateView.as_view(), name="add", ),
    
    path('change/', views.BookmarkChangeLV.as_view(), name="change", ),
    
    path('<int:pk>/update/', views.BookmarkUpdateView.as_view(), name="update", ),
    
    path('<int:pk>/delete/', views.BookmarkDeleteView.as_view(), name="delete", ),
    
]