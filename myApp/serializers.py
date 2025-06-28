from rest_framework import serializers
from .models import Recipe, RecipeIngredient, Rating, Favorite, Category, Ingredient


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ['id', 'name']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'amount']


class RecipeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    # recipe_ingredients is the related_name for recipe foreinkey in RecipeIngredient Model
    recipe_ingredients = RecipeIngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ['recipe_id', 'title', 'instructions', 'picture_url', 'category', 'recipe_ingredients']


