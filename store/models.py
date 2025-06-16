from django.db import models
from django.urls import reverse

from user.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name if not self.parent else f"{self.parent} > {self.name}"

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount =  models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    stock_quantity = models.PositiveIntegerField()
    featured_image = models.ImageField(upload_to='product-images/')
    SKU = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse("product-details", args=[self.id, self.slug])
    
    def get_discounted_price(self):
        return self.price * (1 - self.discount / 100) if self.discount else self.price

    def __str__(self):
        return self.name
        
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product-images/')


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

                                                                                                                                                                        
