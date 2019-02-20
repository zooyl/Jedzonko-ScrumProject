from datetime import datetime
from django.shortcuts import render
from django.views import View


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)

def index(request):
    return render(request,'index.html')

def main(request):
    return render(request,'dashboard.html')
#
# def land(request):
#
# def recipe(request):
#
# def recipe_list(request):
#
# def add_recipe(request):
#
# def edit_recipe(request):
#
# def plan(request):
#
def plan(request):
    return render(request,'app-schedules.html')

def list(request):
    return render(request,'app-recipes.html')

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')