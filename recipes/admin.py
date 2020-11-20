from django.contrib import admin
from .models import Recipe


# Register your models here.
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'price',
        'time',
        'image',
    )

    ordering = ('name',)


admin.site.register(Recipe, RecipeAdmin)
