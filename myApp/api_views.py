from rest_framework import viewsets
from .models import Recipe
from .serializers import RecipeSerializer
from rest_framework import filters



class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'ingredients__name']

    # TODO: Users can filter like this:
    # http://127.0.0.1:8000/api/v1/recipes/?search=Sprite