from django.shortcuts import render, redirect
from django.views import generic
import requests

from .models import Amount, Category, Rating, Recipe, Ingredient



# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'myApp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = requests.get("https://www.thecocktaildb.com/api/json/v1/1/random.php")
        response.raise_for_status()
        drink = response.json()
        context['drink'] = drink['drinks'][0]
        return context


class SearchView(generic.TemplateView):
    template_name = 'myApp/search.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        drinks = None

        if query:
            url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={query}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                drinks = response.json()['drinks']
                if not drinks:  # Handle case where no drinks are found
                    drinks = {"error": "No drinks found for this search!"}
            except:
                drinks = {"error": "An Error happened!!! Try Another Time!"}
        return render(request, self.template_name, {'query': query, 'drinks': drinks})



def add_to_favorite(request, pk):    
    url = f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={pk}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        drink = response.json()['drinks'][0]
        if not drink:  # Handle case where no drinks are found
            drink = {"error": "No drinks found for this search!"}
    except:
        drink = {"error": "An Error happened!!! Try Another Time!"}
        
    print(drink)
    if drink:
        if Recipe.objects.filter(recipe_id=drink['idDrink']).exists():
            print("we've already had this item in the database.")
        else:
            print("we don't have this drink in the database and we should add it.")
            ingredients_list = []
            amounts_list = []
            for number in range(1, 16):
                if drink[f'strMeasure{number}'] is None:
                    break
                else:                    
                    ingredients_list.append(drink[f'strIngredient{number}'])
                    amounts_list.append(drink[f'strMeasure{number}'])

            drink_category, _ =  Category.objects.get_or_create(title=drink['strCategory'])
            recipe = Recipe.objects.create(recipe_id=drink['idDrink'],
                                    title=drink['strDrink'],
                                    instruction=drink['strInstructions'],
                                    category=drink_category,
                                    picture_url=drink['strDrinkThumb'],)   
            
            for index in range(len(amounts_list)):
                ingredient, _ = Ingredient.objects.get_or_create(title=ingredients_list[index])
                amount, _ = Amount.objects.get_or_create(title=amounts_list[index])
                recipe.ingredients.add(ingredient)
                recipe.amounts.add(amount)
   
    return redirect('search')

