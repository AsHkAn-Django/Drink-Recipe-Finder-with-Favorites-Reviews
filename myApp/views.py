from django.shortcuts import render
from django.views.generic import TemplateView
import requests


# Create your views here.
class IndexView(TemplateView):
    template_name = 'myApp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = requests.get("https://www.thecocktaildb.com/api/json/v1/1/random.php")
        response.raise_for_status()
        drink = response.json()
        context['drink'] = drink['drinks'][0]
        return context


class SearchView(TemplateView):
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
            except:
                drink = {"error": "Not Found!!! Try Something Else!"}
        return render(request, self.template_name, {'query': query, 'drinks': drinks})
