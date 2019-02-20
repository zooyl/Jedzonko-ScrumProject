from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View
from jedzonko.models import JedzonkoPlan


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class PlanAdd(View):
    def get(self, request):
        return render(request, 'app-add-schedules.html')

    def post(self, request):
        plan_name = request.POST['plan_name']
        description = request.POST['description']
        JedzonkoPlan.objects.create(name=plan_name, description=description)
        return redirect('/plan/add/details')