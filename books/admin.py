from django.contrib import admin
# from books.models import *

from django.apps import apps

# Register your models here.

# Registering all the models in one go.

# models_list = [Author, Publisher, Book, Like, Rating, Comment]
# admin.site.register(models_list)

# or Another approach

# apps.all_models['app_name'] -> returns a dict with the values being the models belonging to that app.

admin.site.register(apps.all_models['books'].values())