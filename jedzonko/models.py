from django.db import models

days = (
    (0, 'Poniedzialek'),
    (1, 'Wtorek'),
    (2, 'Sroda'),
    (3, 'Czwartek'),
    (4, 'Piatek'),
    (5, 'Sobota'),
    (6, 'Niedziela'),
)


class JedzonkoRecipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField(null=True)
    created = models.TimeField(auto_now_add=True)
    updated = models.TimeField(auto_now_add=True)
    preparation_time = models.IntegerField()
    votes = models.IntegerField(null=True)
    way_of_preparing = models.TextField(null=True)

    def __str__(self):
        return f'{self.id},{self.name},{self.ingredients},{self.description}, {self.created}, {self.updated},' \
            f'{self.preparation_time},{self.votes}'


class JedzonkoPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    created = models.DateField(auto_now_add=True)


class JedzonkoDayname(models.Model):
    day_name = models.IntegerField(choices=days)
    order = models.IntegerField(null=True)


class JedzonkoRecipeplan(models.Model):
    meal_name = models.CharField(max_length=255)
    order = models.IntegerField()
    day_name_id = models.ForeignKey(JedzonkoDayname, on_delete=models.DO_NOTHING)
    plan_id = models.ForeignKey(JedzonkoPlan, on_delete=models.DO_NOTHING)
    recipe_id = models.ForeignKey(JedzonkoRecipe, on_delete=models.DO_NOTHING)


class JedzonkoPage(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255, blank=True)
