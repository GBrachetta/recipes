from django import forms

# from .widgets import CustomClearableFileInput
from .models import Recipe
from .widgets import CustomClearableFileInput


class RecipeForm(forms.ModelForm):
    """Recipe form"""

    class Meta:
        model = Recipe
        fields = (
            "name",
            "description",
            "instructions",
            "price",
            "time",
            "image",
        )

    image = forms.ImageField(
        label="Image", required=False, widget=CustomClearableFileInput
    )

    thumbnail = image.hidden_widget
