from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View
import random
from jedzonko.models import JedzonkoPlan, JedzonkoRecipe, JedzonkoRecipeplan, days
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


def contact(request):
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')


class PlanAdd(View):
    def get(self, request):
        return render(request, 'app-add-schedules.html')

    def post(self, request):
        plan_name = request.POST.get('plan_name')
        description = request.POST.get('description')
        JedzonkoPlan.objects.create(name=plan_name, description=description)
        return redirect('/plan/add/details')


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
        return render(request, 'recipes.html', ctx)


class RecipesList(View):

    def get(self, request):
        sorting = JedzonkoRecipe.objects.all().order_by('-votes')
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


class PlanList(View):

    def get(self, request):
        sorting = JedzonkoPlan.objects.all().order_by('name')
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
        return render(request, 'app-schedules.html', ctx)

    def post(self, request):
        return render(request, 'app-schedules.html')


class PlanDetails(View):

    def get(self, request):
        var = JedzonkoRecipeplan.objects.all().filter(pk=4)  # zamienic 4ke na zalezna od wyboru planu przez usera
        for i in var:
            y = i.meal_name
        przepis = JedzonkoRecipe.objects.all()
        ctx = {
            'nazwa_planu': y,
            'przepis': przepis,
            'dzien': days
        }
        return render(request, 'app-schedules-meal-recipe.html', ctx)

    def post(self, request):
        var = JedzonkoRecipeplan.objects.all().filter(pk=4)
        for i in var:
            y = i.id
        przepis = JedzonkoRecipe.objects.all()
        name = request.POST.get('fname')
        order = request.POST.get('fnumber')
        recipe_name = request.POST.get('frecipe')
        day = request.POST.get('fday')
        if '' in (var, name):
            ctx = {
                'message': 'Uzupelnij pola',
                'nazwa_planu': y,
                'przepis': przepis,
                'dzien': days

            }
            return render(request, 'app-schedules-meal-recipe.html', ctx)
        ctx = {
            'message': 'Przepis zapisany',
            'nazwa_planu': y,
            'dzien': days,
            'przepis': przepis
        }
        JedzonkoRecipeplan.objects.create(meal_name=name, order=order, recipe_id_id=recipe_name, day_name_id_id=day[0],
                                          plan_id_id=y,)
        return render(request, 'app-schedules-meal-recipe.html', ctx)


def recipe_details(request):
    recipe = JedzonkoRecipe.objects.latest('id')
    return render(request, 'app-recipe-details.html', {'recipe': recipe})
