# Generated by Django 2.1.2 on 2019-02-23 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jedzonkorecipeplan',
            name='day_name_id',
        ),
        migrations.AddField(
            model_name='jedzonkopage',
            name='slug',
            field=models.SlugField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='jedzonkorecipeplan',
            name='day_name',
            field=models.IntegerField(choices=[(0, 'Poniedzialek'), (1, 'Wtorek'), (2, 'Sroda'), (3, 'Czwartek'), (4, 'Piatek'), (5, 'Sobota'), (6, 'Niedziela')], null=True),
        ),
        migrations.AlterField(
            model_name='jedzonkorecipe',
            name='updated',
            field=models.TimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='jedzonkorecipe',
            name='votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='jedzonkorecipeplan',
            name='plan_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedzonko.JedzonkoPlan'),
        ),
        migrations.AlterField(
            model_name='jedzonkorecipeplan',
            name='recipe_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedzonko.JedzonkoRecipe'),
        ),
        migrations.DeleteModel(
            name='JedzonkoDayname',
        ),
    ]
