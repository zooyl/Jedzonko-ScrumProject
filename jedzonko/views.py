from datetime import datetime

from django.shortcuts import render
from django.views import View
from jedzonko.models import JedzonkoRecipe
import random


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class Randomize(View):

    def get(self, request):
        ctx = {}
        self.lista = []
        var = JedzonkoRecipe.objects.all()
        for v in var:
            if v.name is not None:
                self.lista.append(v.id)
        self.choose = random.sample(self.lista, 3)
        for i in range(0, 3):
            x = self.choose[i]
            show_it = JedzonkoRecipe.objects.get(id=x)
            ctx[f'title{i}'] = show_it.name
            ctx[f'losuj{i}'] = show_it.description
        return render(request, 'index.html', ctx)


class Form(View):
    def add_recipe(self):
        pass

    def get(self, request):
        return render(request, 'app-add-recipe.html', )

    def post(self, request):
        name = request.POST.get('recipe_name')
        description = request.POST.get('description')
        preparing_time = request.POST.get('preparing_time')
        way_of_preparing = request.POST.get('way_of_preparing')
        ingedients = request.POST.get('ingredients')
        if None in (name, description, preparing_time, way_of_preparing, ingedients):
            ctx = {
                'message' : 'Uzupelnij pola'
            }
            return render(request, 'app-add-recipe.html', ctx)


'''Po wejściu na stronę `/recipe/add` metodą GET powininen pojawić się formularz, w którym można dodać nowy przepis.

Pola formularza:

- nazwa przepisu (pole typu text),
- opis przepisu (pole typu text),
- czas przygotowania w minutach (pole typu number),
- sposób przygotowania (pole typu textarea),
- składniki (pole typu textarea).

Formularz musi posiadać przycisk „wyślij”, po naciśnięciu którego ma zostać wysłany metodą POST na stronę `/recipe/add`.

Należy dodać odpowiedni wpis w pliku urls.py'''
