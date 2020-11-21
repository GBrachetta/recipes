from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RecipeForm
from .models import Recipe


# Create your views here.
def recipes(request):
    """Renders the recipes page"""

    all_recipes = Recipe.objects.all().order_by("-name")
    context = {"recipes": all_recipes, "recipe": "active"}
    return render(request, "recipes/recipes.html", context)


def recipe_detail(request, recipe_id):
    """Display a single recipe"""
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    context = {"recipe": recipe, "recipes": "active"}
    template = "recipes/recipe.html"

    return render(request, template, context)


@login_required
def add_recipe(request):
    """Add recipe"""

    if not request.user.is_superuser:
        messages.error(request, "Reserved to administrators.")
        return redirect(reverse("recipes"))

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Recipe added.")
            return redirect(reverse("recipes"))

        messages.error(request, "Failed to add recipe. Please check the form.")
    else:
        form = RecipeForm()

    template = "recipes/add_recipe.html"
    context = {"form": form, "recipes": "active"}

    return render(request, template, context)
