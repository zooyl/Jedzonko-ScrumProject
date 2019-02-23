from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jedzonkopage',
            name='slug',
            field=models.SlugField(null=True, max_length=255),
        ),
    ]
