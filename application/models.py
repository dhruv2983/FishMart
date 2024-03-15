from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom user model to accommodate both buyers and sellers
class User(AbstractUser):
    is_seller = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

# Model for products being sold
class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    address = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=10, choices=(('card', 'Card'), ('cash', 'Cash')))
    card_number = models.CharField(max_length=16, blank=True, null=True, default=None)
    expiry_date = models.DateField(blank=True, null=True , default=None)
    cvv = models.CharField(max_length=3, blank=True, null=True , default=None)
    date = models.DateTimeField(auto_now_add=True)
    delivery_method = models.CharField(max_length=10, choices=(('pickup', 'Pickup'), ('delivery', 'Delivery')))