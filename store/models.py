from django.db import models

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()  # Number of units (e.g., 1 bundle, 250 gm)
    unit = models.CharField(max_length=50, choices=[  # Unit of measurement (bundle, kg, gm, etc.)
        ('bundle', 'Bundle'),
        ('kg', 'Kilogram'),
        ('gm', 'Gram'),
        ('piece', 'Piece'),
    ], default='piece')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    special_offer = models.TextField()  # To mark products with special offers
    is_available = models.BooleanField(default=True)  # ← ADD THIS

    def __str__(self):
        return self.name

    def display_quantity(self):
        """ Return a string representation of the quantity and unit """
        return f"{self.quantity} {self.unit}"

    
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # ← Add this line
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Order #{self.id} by {self.name}"


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    message = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

from .models import Product, Order  # if Order is defined elsewhere

from django.contrib.auth.models import User

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def item_total(self):
        return self.product.price * self.quantity



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # snapshot of price at order time

    def __str__(self):
        return f"{self.quantity} x {self.product.name} @ {self.price}"