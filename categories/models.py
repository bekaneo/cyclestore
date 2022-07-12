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

# class Size(models.Model):
#     size_in_inch = models.IntegerField()
#     size_in_cm = models.CharField(max_length=100)
#     slug = models.SlugField(max_length=100, blank=True)

#     def __str__(self):
#         return self.size_in_inch
    
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(str(self.size_in_inch))
#         super().save(*args, **kwargs)

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategory')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.name))
        super().save(*args, **kwargs)



