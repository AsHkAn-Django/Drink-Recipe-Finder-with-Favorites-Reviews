from rest_framework import viewsets
from .models import Recipe
from .serializers import RecipeSerializer



class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer