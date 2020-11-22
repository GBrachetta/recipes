from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import RecipeForm
from .models import Recipe


# Create your views here.
def recipes(request):
    """Renders the recipes page"""

    recipes = Recipe.objects.all().order_by("-name")
    paginator = Paginator(recipes, 8)
    page = request.GET.get("page")
    paged_recipes = paginator.get_page(page)

    context = {"recipes": paged_recipes, "recipe": "active"}
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


@login_required
def edit_recipe(request, recipe_id):
    """Edit an existing recipe"""
    if not request.user.is_superuser:
        messages.error(request, "Reserved to administrators.")
        return redirect(reverse("home"))

    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated recipe.")
            return redirect(reverse("recipes"))
        else:
            messages.error(request, "Failed to update. Please check the form.")
    else:
        form = RecipeForm(instance=recipe)

    template = "recipes/edit_recipe.html"
    context = {"form": form, "recipe": recipe, "recipes": "active"}

    return render(request, template, context)


@login_required
def delete_recipe(request, recipe_id):
    """Delete a recipe"""
    if not request.user.is_superuser:
        messages.error(request, "Reserved to administrators.")
        return redirect(reverse("recipes"))
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe.delete()
    messages.success(request, "Recipe deleted.")
    return redirect(reverse("recipes"))


def search(request):
    """Performs search by keyword"""

    recipes = Recipe.objects.all()
    query = None

    if request.GET:
        if "keywords" in request.GET:
            query = request.GET["keywords"]
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!"
                )
                return redirect(reverse("recipes"))

            queries = Q(name__icontains=query) | Q(
                description__icontains=query
            )
            recipes = recipes.filter(queries)

    template = "recipes/recipes.html"
    context = {
        "recipes": recipes,
        "search_term": query,
        "from_search": True,
    }

    return render(request, template, context)
