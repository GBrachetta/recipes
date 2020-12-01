from django.contrib import admin
from .models import Recipe, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    ordering = ("name",)


class RecipeAdmin(admin.ModelAdmin):
    """Admin control of recipes"""

    list_display = (
        "name",
        "difficulty",
        "created",
        "price",
        "time",
        "thumbnail_preview",
    )

    readonly_fields = ("thumbnail",)

    ordering = ("name",)

    def thumbnail_preview(self, obj):
        """summary_line"""

        return obj.thumbnail_preview

    thumbnail_preview.short_description = "Thumbnail"
    thumbnail_preview.allow_tags = True


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category, CategoryAdmin)
