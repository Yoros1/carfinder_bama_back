''' docstring '''
from django.urls import path
from main import views

app_name = 'main'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='HomePage'),
    path('SearchResult/', views.search_result, name='search_result')
]
