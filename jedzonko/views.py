from datetime import datetime
from jedzonko.models import jedzonko_dayname,jedzonko_recipe,jedzonko_plan,jedzonko_page,jedzonko_recipeplan
from django.shortcuts import render
from django.views import View


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)

def main(request):

def land(request):

def recipe(request):

def recipe_list(request):

def add_recipe(request):

def edit_recipe(request):

def plan(request):

def add_plan(request):

def add_details_plan(request):

def contact(request):

def about(request):
