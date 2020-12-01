from django import forms

# from .widgets import CustomClearableFileInput
from .models import Recipe
from .widgets import CustomClearableFileInput


class RecipeForm(forms.ModelForm):
    """Recipe form"""

    class Meta:
        model = Recipe
        fields = (
            "category",
            "name",
            "description",
            "instructions",
            "difficulty",
            "price",
            "time",
            "image",
            "tags",
        )
        widgets = {"tags": forms.TextInput(attrs={"data-role": "tagsinput"})}

    image = forms.ImageField(
        label="Image", required=False, widget=CustomClearableFileInput
    )

    thumbnail = image.hidden_widget
