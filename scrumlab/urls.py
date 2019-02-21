"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, re_path
from jedzonko.views import IndexView, Randomize, Form, PlanAdd, RecipesList, recipe_details

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', IndexView.as_view()),

    # re_path(r'$',index),
    # re_path(r'main/$',main),
    # re_path(r'recipe/list/$', list),
    # re_path(r'recipe/add/$',),
    # re_path(r'recipe/modify/$',),
    # re_path(r'plan/(\d)*', plan),
    re_path(r'plan/add', PlanAdd.as_view()),
    # re_path(r'plan/add/details/$',),
    # re_path(r'contact/$', contact),
    # re_path(r'about', about),
    path('', Randomize.as_view()),
    path('recipe/add', Form.as_view()),
    path('plan/list', RecipesList.as_view()),
    path('recipe/', recipe_details),
]
