from django.urls import path
from .views import IndexView, SearchView

urlpatterns = [
    path('search', SearchView.as_view(), name='search'),
    path('', IndexView.as_view(), name='index'),
]