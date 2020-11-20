from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    time = models.IntegerField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
