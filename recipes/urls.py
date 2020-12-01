from django.urls import path
from . import views

urlpatterns = [
    path("", views.recipes, name="recipes"),
    path("add_recipe/", views.add_recipe, name="add_recipe"),
    path("add_category/", views.add_category, name="add_category"),
    path("<int:recipe_id>/", views.recipe_detail, name="recipe_detail"),
    path(
        "edit_recipe/<int:recipe_id>/",
        views.edit_recipe,
        name="edit_recipe",
    ),
    path(
        "edit_category/<int:category_id>/",
        views.edit_category,
        name="edit_category",
    ),
    path(
        "delete_recipe/<int:recipe_id>/",
        views.delete_recipe,
        name="delete_recipe",
    ),
    path(
        "delete_category/<int:category_id>/",
        views.delete_category,
        name="delete_category",
    ),
    path("search/", views.search, name="search"),
    path("categories/", views.categories, name="categories")
]
