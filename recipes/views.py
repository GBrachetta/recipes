from django.shortcuts import render


# Create your views here.
def recipes(request):
    """
    Renders the landing page
    """
    context = {"recipes": "active"}
    return render(request, "recipes/recipes.html", context)


def add_recipe(request):
    """Add recipe"""

    return render(request, "recipes/includes/add_recipe.html")
