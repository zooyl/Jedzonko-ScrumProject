from datetime import datetime
from django.shortcuts import render
from django.views import View
import random
from jedzonko.models import JedzonkoPlan, JedzonkoRecipe, JedzonkoPage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


def main(request):
    ilosc_r = JedzonkoPlan.objects.all().count()
    ilosc_p = JedzonkoRecipe.objects.all().count()
    return render(request, 'dashboard.html', {'ilosc_r': ilosc_r, 'ilosc_p': ilosc_p})


def plan(request):
    return render(request, 'app-schedules.html')


def lista_planow(request):
    return render(request, 'app-schedules.html')


def contact(request):
    content = JedzonkoPage.objects.filter(slug="contact")
    if content.exists():
        return render(request, 'contact.html', {'content': content})
    else:
        empty = "Strona w przygotowaniu"
        return render(request, 'contact.html', {'empty': empty})


def about(request):
    content = JedzonkoPage.objects.filter(slug="about")
    if content.exists():
        return render(request, 'about.html', {'content': content})
    else:
        empty = "Strona w przygotowaniu"
        return render(request, 'about.html', {'empty': empty})


class PlanAdd(View):
    def get(self, request):
        return render(request, 'app-add-schedules.html')

    def post(self, request):
        plan_name = request.POST.get('plan_name')
        description = request.POST.get('description')
        JedzonkoPlan.objects.create(name=plan_name, description=description)
        finish = "Plan dodany"
        return render(request, 'app-add-schedules.html', {'finish': finish})


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
    def get(self, request):
        return render(request, 'app-add-recipe.html', )

    def post(self, request):
        name = request.POST.get('recipe_name')
        description = request.POST.get('description')
        preparing_time = request.POST.get('preparing_time')
        way_of_preparing = request.POST.get('way_of_preparing')
        ingedients = request.POST.get('ingredients')
        if '' in (name, description, preparing_time, way_of_preparing, ingedients):
            ctx = {
                'message': 'Uzupelnij pola'
            }
            return render(request, 'app-add-recipe.html', ctx)
        JedzonkoRecipe.objects.create(name=name, description=description, ingredients=ingedients,
                                      preparation_time=preparing_time, way_of_preparing=way_of_preparing)
        ctx = {
            'message': 'Przepis zapisany'
        }
        return render(request, 'app-add-recipe.html', ctx)


class RecipesList(View):

    def get(self, request):
        sorting = JedzonkoRecipe.objects.all().order_by('name')
        paginator = Paginator(sorting, 50)
        page = request.GET.get('page', 1)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        ctx = {
            'sorting': sorting,
            'users': users
        }
        return render(request, 'recipes.html', ctx)

    def post(self, request):
        return render(request, 'recipes.html')


def recipe_details(request, id):
    recipe = JedzonkoRecipe.objects.get(id=id)


def recipe_details(request):
    recipe = JedzonkoRecipe.objects.latest('id')
    return render(request, 'app-recipe-details.html', {'recipe': recipe})
