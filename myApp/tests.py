from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Recipe, Ingredient, RecipeIngredient


class RecipeViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

        self.ingredient1 = Ingredient.objects.create(name="Sprite")
        self.ingredient2 = Ingredient.objects.create(name="Sugar")

        self.recipe1 = Recipe.objects.create(
            recipe_id=1,
            title="Lemonade",
            instructions="Mix well",
            picture_url="http://example.com/pic1.jpg",
        )
        RecipeIngredient.objects.create(
            recipe=self.recipe1, ingredient=self.ingredient1, amount="100ml", order=1
        )

        self.recipe2 = Recipe.objects.create(
            recipe_id=2,
            title="Sweet Tea",
            instructions="Brew tea and add sugar",
            picture_url="http://example.com/pic2.jpg",
        )
        RecipeIngredient.objects.create(
            recipe=self.recipe2, ingredient=self.ingredient2, amount="2 tsp", order=1
        )

    def test_favorite_toggle(self):
        # Try to favorite without auth -> should be unauthorized
        url = f"/api/v1/recipes/{self.recipe1.pk}/favorite/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticate
        self.client.login(username="testuser", password="testpass")

        # Favorite the recipe
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Favorite", response.data)

        # Try to favorite again (should unfavorite)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Unfavorite", response.data)

    def test_search_filter(self):
        # Search by ingredient name 'Sprite'
        url = "/api/v1/recipes/?search=Sprite"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Only recipe1 should be returned because it has ingredient 'Sprite'
        returned_titles = [r["title"] for r in response.data["results"]]
        self.assertIn("Lemonade", returned_titles)
        self.assertNotIn("Sweet Tea", returned_titles)
