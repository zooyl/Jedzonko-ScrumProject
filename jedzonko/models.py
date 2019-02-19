from django.db import models

class Page(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    slug=models.CharField(max_length=255)

class Recipe(models.Model):
    name=models.CharField(max_length=255)
    ingredients=models.TextField()
    description=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    preparation_time=models.IntegerField()
    votes=models.IntegerField()

class Day_name(models.Model):
    day_name=models.CharField(max_length=16)
    order=models.IntegerField()

class Plan(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField()
    created=models.DateTimeField(auto_now_add=True)

class Recipe_plan(models.Model):
    meal_name=models.CharField(max_length=255)
    order=models.IntegerField()
    day_name_id=models.ForeignKey(jedzonko_dayname,on_delete=models.CASCADE)
    plan_id=models.ForeignKey(jedzonko_plan,on_delete=models.CASCADE)
    recipe_id=models.ForeignKey(jedzonko_recipe,on_delete=models.CASCADE)
