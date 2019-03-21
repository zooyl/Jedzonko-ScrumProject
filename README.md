# Jedzonko
Jedzonko is a meal manager, that let users create recipes and schedules with additional details to them.
You can see last added plan in dashboard and vote for recipes.
Made in SCRUM.

# It's live!
Check it out at: https://jedzonko-scrum.herokuapp.com/

### Installing

These instructions will get you a copy of the project up and running.
Create virtual environment on your machine, then install requirements using:

```
pip install -r requirements.txt
```
### Important
In ```scrumlab``` folder, update ```local_settings.py.txt```  to your settings and delete ```.txt``` from the end
of a file.

Open terminal in ```manage.py``` directory and type ```python manage.py migrate```.
After that, fill database using ```python manage.py loaddata jedzonko``` , finally you can start server by ```python manage.py runserver``` command.

### Preview
## Landing Page:

![Landing](https://github.com/zooyl/Jedzonko-ScrumProject/blob/master/preview/LandingPage.png?raw=true)

## Dashboard:

![Dashboard](https://github.com/zooyl/Jedzonko-ScrumProject/blob/master/preview/Dashboard.png?raw=true)

## Recipes List:

![List](https://github.com/zooyl/Jedzonko-ScrumProject/blob/master/preview/ListaPrzepisow.png?raw=true)

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
