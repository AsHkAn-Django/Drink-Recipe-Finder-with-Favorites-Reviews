from django.urls import path
from .views import *

urlpatterns = [
    path('add_to_favorite/<int:pk>', add_to_favorite, name='add_favorite'),
    path('search', SearchView.as_view(), name='search'),
    path('my_favorites/', my_favorites, name='my_favorites'),
    path('', IndexView.as_view(), name='index'),
]