from django.contrib import admin
from .models import Amount, Category, Rating, Recipe, Ingredient


admin.site.register(Amount)
admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(Recipe)
admin.site.register(Ingredient)