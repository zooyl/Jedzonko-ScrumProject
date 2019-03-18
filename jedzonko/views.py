from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View
import random
from jedzonko.models import JedzonkoPlan, JedzonkoRecipe, JedzonkoRecipeplan, days, JedzonkoPage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


def main(request):
    check = JedzonkoPlan.objects.all()
    if check.exists():
        ostatni = JedzonkoPlan.objects.all().latest('id')
        ilosc_p = JedzonkoPlan.objects.all().count()
        ilosc_r = JedzonkoRecipe.objects.all().count()
        przpisy = []
        for day in range(7):
            przpisy.append(JedzonkoRecipeplan.objects.filter(plan_id=ostatni, day_name=day))
        return render(request, 'dashboard.html',
                      {'ilosc_r': ilosc_r, 'ilosc_p': ilosc_p, 'ostatni': ostatni, 'przpisy_dla_dnia': przpisy})
    else:
        return render(request, 'dashboard.html')


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
        if '' in (plan_name, description):
            warning = "Uzupelnij wszystkie pola"
            return render(request, 'app-add-schedules.html', {'warning': warning})
        else:
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
        if len(self.lista) < 3:
            return render(request, 'index.html')
        else:
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
        qs = JedzonkoRecipe.objects.all().order_by("-votes", "-created")
        paginator = Paginator(qs, 15)
        page_number = request.GET.get("page")

        if page_number is None:
            page_number = 1
        elif int(page_number) > paginator.num_pages:
            raise Http404("Podana strona nie istnieje!")
        page_number = int(page_number)
        start_index = page_number - 5 if page_number >= 5 else 0
        end_index = page_number + 5 if page_number <= paginator.num_pages - 5 else paginator.num_pages
        page_range = paginator.page_range[start_index:end_index]
        return render(request, "recipes.html", {"recipes": paginator.page(page_number), "page_range": page_range})


class PlanList(View):

    def get(self, request):
        qs = JedzonkoPlan.objects.all().order_by('name')
        paginator = Paginator(qs, 15)
        page_number = request.GET.get("page")

        if page_number is None:
            page_number = 1
        elif int(page_number) > paginator.num_pages:
            raise Http404("Podana strona nie istnieje!")
        page_number = int(page_number)
        start_index = page_number - 5 if page_number >= 5 else 0
        end_index = page_number + 5 if page_number <= paginator.num_pages - 5 else paginator.num_pages
        page_range = paginator.page_range[start_index:end_index]
        return render(request, "app-schedules.html", {"plans": paginator.page(page_number), "page_range": page_range})

class PlanDetails(View):

    def get(self, request, id):
        try:
            var = JedzonkoPlan.objects.get(pk=id)
            y = var.name
            przepis = JedzonkoRecipe.objects.all()
            ctx = {
                'ktory':['śniadanie','drugie śniadanie','obiad','podwieczorek','kolacja','przekąska'],
                'nazwa_planu': y,
                'przepis': przepis,
                'dzien': days
            }
            return render(request, 'app-schedules-meal-recipe.html', ctx)
        except JedzonkoPlan.DoesNotExist:
            raise Http404("Taki plan nie istnieje")

    def post(self, request, id):
        try:
            var = JedzonkoPlan.objects.get(pk=id)
            y = var.id
            przepis = JedzonkoRecipe.objects.all()
            name = request.POST.get('fname')
            order = request.POST.get('forder')
            recipe_name = request.POST.get('frecipe')
            day = request.POST.get('fday')
            if '' in (name, order):
                ctx = {
                    'ktory': ['śniadanie', 'drugie śniadanie', 'obiad', 'podwieczorek', 'kolacja', 'przekąska'],
                    'message': 'Uzupelnij pola',
                    'nazwa_planu': y,
                    'przepis': przepis,
                    'dzien': days

                }
                return render(request, 'app-schedules-meal-recipe.html', ctx)
            ctx = {
                'ktory': ['śniadanie', 'drugie śniadanie', 'obiad', 'podwieczorek', 'kolacja', 'przekąska'],
                'message': 'Przepis dodany do planu',
                'nazwa_planu': y,
                'dzien': days,
                'przepis': przepis
            }
            ''.join(day)
            JedzonkoRecipeplan.objects.update_or_create(meal_name=name, order=order, day_name=day,
                                                        recipe_id_id=recipe_name, plan_id_id=y)
            return render(request, 'app-schedules-meal-recipe.html', ctx)
        except IntegrityError:
            return redirect('/recipe/add')


def recipe_details(request, id):
    try:
        recipe = JedzonkoRecipe.objects.get(id=id)
        if request.method == "POST":
            if request.POST.get('like'):
                recipe.votes += 1
            else:
                recipe.votes -= 1
        recipe.save()
        return render(request, 'app-recipe-details.html', {'recipe': recipe})
    except JedzonkoRecipe.DoesNotExist:
        raise Http404("Taki przepis nie istnieje")


class Modify(View):

    def get(self, request, id):
        try:
            recipe = JedzonkoRecipe.objects.get(id=id)
        except JedzonkoRecipe.DoesNotExist:
            raise Http404("Taki przepis nie istnieje")
        return render(request, 'app-edit-recipe.html', {'recipe': recipe})

    def post(self, request, id):
        recipe = JedzonkoRecipe.objects.get(id=id)
        name = request.POST['name']
        description = request.POST['description']
        preparation_time = request.POST['preparation_time']
        way_of_preparing = request.POST['way_of_preparing']
        ingredients = request.POST['ingredients']
        if '' in (name, description, preparation_time, way_of_preparing, ingredients):
            warning = "Uzupelnij wszystkie pola"
            return render(request, 'app-edit-recipe.html', {'recipe': recipe, 'warning': warning})
        else:
            recipe.name = name
            recipe.description = description
            recipe.preparation_time = preparation_time
            recipe.way_of_preparing = way_of_preparing
            recipe.ingredients = ingredients
            recipe.save()
            finish = "Przepis zaktualizowany"
            return render(request, 'app-edit-recipe.html', {'recipe': recipe, 'finish': finish})


def del_recipe(request, id):
    try:
        recipe = JedzonkoRecipe.objects.get(id=id)
        recipe.delete()
        return redirect('/recipe/list')
    except JedzonkoRecipe.DoesNotExist:
        raise Http404("Taki przepis nie istnieje")


def del_plan(request, id):
    try:
        plan = JedzonkoPlan.objects.get(id=id)
        plan.delete()
        return redirect('/plan/list')
    except JedzonkoPlan.DoesNotExist:
        raise Http404("Taki plan nie istnieje")


def plan_details(request, id):
    try:
        day = days
        plan = JedzonkoPlan.objects.all().get(id=id)
        schedule = JedzonkoRecipeplan.objects.filter(plan_id=id).order_by('day_name')
        return render(request, 'app-details-schedules.html', {'plan': plan, 'schedule': schedule, 'day': day})
    except ObjectDoesNotExist:
        raise Http404('Taki plan nie istnieje')


def details_delete(request, id_schedule, id_plan):
    try:
        schedule = JedzonkoRecipeplan.objects.get(id=id_schedule)
        schedule.delete()
        return redirect(f'/plan/{id_plan}')
    except ObjectDoesNotExist:
        raise Http404('Taki plan nie istnieje')


class EditPlan(View):

    def get(self, request, id):
        try:
            plan = JedzonkoPlan.objects.get(id=id)
        except JedzonkoPlan.DoesNotExist:
            raise Http404("Taki plan nie istnieje")
        return render(request, 'app-edit-schedules.html', {'plan': plan})

    def post(self, request, id):
        plan = JedzonkoPlan.objects.get(id=id)
        name = request.POST['name']
        description = request.POST['description']
        if '' in (name, description):
            warning = "Uzupelnij wszystkie pola"
            return render(request, 'app-edit-schedules.html', {'plan': plan, 'warning': warning})
        else:
            plan.name = name
            plan.description = description
            plan.save()
            finish = "Przepis zaktualizowany"
            return render(request, 'app-edit-schedules.html', {'plan': plan, 'finish': finish})

