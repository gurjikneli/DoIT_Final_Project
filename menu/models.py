from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Dish(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    spicy_level = models.IntegerField(default=0)
    has_nuts = models.BooleanField(default=False)
    is_vegetarian = models.BooleanField(default=False)
    image = models.ImageField(upload_to='dishes/')

    def __str__(self):
        return self.name