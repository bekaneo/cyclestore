from django.db import models
from slugify import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.name))
        super().save(*args, **kwargs)


class Brand(models.Model):
    brand = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)

    def __str__(self):
        return self.brand

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.brand))
        super().save(*args, **kwargs)


class Size(models.Model):
    size_in_inch = models.CharField(max_length=10)
    size_in_cm = models.CharField(max_length=20)

    def __str__(self):
        return self.size_in_cm


