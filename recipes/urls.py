from django.urls import path
from . import views

urlpatterns = [
    path("", views.recipes, name="recipes"),
    path("add_recipe/", views.add_recipe, name="add_recipe"),
    path("<int:recipe_id>/", views.recipe_detail, name="recipe_detail"),
]
