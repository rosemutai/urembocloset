from django.db import models
from user.models import User
from store.models import Product

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def calculate_product_cost(self):
        total = self.product.price * self.quantity
        return total


# class Payment(models.Model):
#     order = models.OneToOneField(Order, on_delete=models.CASCADE)
#     payment_method = models.CharField(max_length=50, choices=(
#         ('card', 'card'),
#         ('M-Pesa', 'M-pesa')
#     ))
#     transaction_id = models.CharField(max_length=100)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20, choices=(
#         ('success', 'success'),
#         ('failed', 'failed')
#     ))
#     paid_at = models.DateTimeField(null=True, blank=True)