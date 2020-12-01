from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.template.defaultfilters import slugify
from django.db.models import Q
from .forms import RecipeForm, CategoryForm
from .models import Category, Recipe


# Create your views here.
def recipes(request):
    """Renders the recipes page"""

    recipes = Recipe.objects.all().order_by("-name")
    paginator = Paginator(recipes, 8)
    page = request.GET.get("page")
    paged_recipes = paginator.get_page(page)

    context = {"recipes": paged_recipes, "recipe": "active"}
    return render(request, "recipes/recipes.html", context)


def categories(request):
    """Renders the categories page"""

    categories = Category.objects.all().order_by("name")

    context = {"categories": categories, "recipe": "active"}
    return render(request, "recipes/categories.html", context)


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
            # form.save()
            # messages.success(request, "Recipe added.")
            # return redirect(reverse("recipes"))
            new_recipe = form.save(commit=False)
            new_recipe.slug = slugify(new_recipe.name)
            new_recipe.save()
            form.save_m2m()
            messages.success(request, "Recipe added.")
            return redirect(reverse("recipes"))

        messages.error(request, "Failed to add recipe. Please check the form.")
    else:
        form = RecipeForm()

    template = "recipes/add_recipe.html"
    context = {"form": form, "recipes": "active"}

    return render(request, template, context)


@login_required
def add_category(request):
    """Add category"""

    if not request.user.is_superuser:
        messages.error(request, "Reserved to administrators.")
        return redirect(reverse("recipes"))

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added.")
            return redirect(reverse("categories"))
        messages.error(request, "Failed to add recipe. Please check the form.")
    else:
        form = CategoryForm()

    template = "recipes/add_category.html"
    context = {"form": form, "recipes": "active"}

    return render(request, template, context)


@login_required
def edit_category(request, category_id):
    """Edit category"""

    if not request.user.is_superuser:
        messages.error(request, "Reserved to administrators.")
        return redirect(reverse("recipes"))

    category = get_object_or_404(Category, pk=category_id)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category edited.")
            return redirect(reverse("categories"))
        messages.error(request, "Failed to update. Please check the form.")
    else:
        form = CategoryForm(instance=category)

    template = "recipes/edit_category.html"
    context = {
        "form": form,
        "category": category,
        "recipes": "active",
    }

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
            # form.save()
            # messages.success(request, "Successfully updated recipe.")
            # return redirect(reverse("recipes"))
            updated_recipe = form.save(commit=False)
            updated_recipe.slug = slugify(updated_recipe.name)
            updated_recipe.save()
            form.save_m2m()
            messages.success(request, "Recipe added.")
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


@login_required
def delete_category(request, category_id):
    """Delete a category"""
    if not request.user.is_superuser:
        messages.error(request, "Reserved to administrators.")
        return redirect(reverse("categories"))
    category = get_object_or_404(Category, pk=category_id)
    category.delete()
    messages.success(request, "Category deleted.")
    return redirect(reverse("categories"))


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
