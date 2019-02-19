from datetime import datetime

from django.shortcuts import render
from django.views import View
from jedzonko.models import JedzonkoRecipe
import random


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class Random:
    lista = []

    def list_it(self):
        var = JedzonkoRecipe.objects.all()
        for v in var:
            self.lista.append(v.id)
        return self.lista

    def random_it(self):
        choose = random.sample(self.lista, 3)
        return choose

    def show_must_go_on(self, request, choose):
        if request.method == 'GET':
            x = choose[0]
            show_it = JedzonkoRecipe.objects.get(id=int(x))
            y = {'losuj': show_it.description}, {'title': show_it.name}
            return render(request, 'index.html', y)
        else:
            x = choose[1]
            show_it = JedzonkoRecipe.objects.get(id=int(x))
            y = {'losuj': show_it.description}, {'title': show_it.name}
            return render(request, 'index.html', y)