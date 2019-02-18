from django.db import models

class jedzonko_page(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    slug=models.CharField(max_length=255)


class jedzonko_recipe(models.Model):
    name=models.CharField(max_length=255)
    ingredients=models.TextField()
    description=models.TextField()
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)
    preparation_time=models.IntegerField()
    votes=models.IntegerField()


class jedzonko_dayname(models.Model):
    day_name=models.CharField(max_length=16)
    order=models.IntegerField()


class jedzonko_plan(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField()
    created=models.DateField()


class jedzonko_recipeplan(models.Model):
    meal_name=models.CharField(max_length=255)
    order=models.IntegerField()
    day_name_id=models.ForeignKey(jedzonko_dayname,on_delete=models.CASCADE)
    plan_id=models.ForeignKey(jedzonko_plan,on_delete=models.CASCADE)
    recipe_id=models.ForeignKey(jedzonko_recipe,on_delete=models.CASCADE)