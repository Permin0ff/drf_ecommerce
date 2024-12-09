from django.db import models

from apps.accounts.models import User
from apps.common.models import BaseModel
from apps.common.utils import generate_unique_code
from apps.shop.models import Product


class ShippingAddress(BaseModel):
    """
    Represents a shipping address associated with a user.

    Attributes:
        user (ForeignKey): The user who owns the shipping address.
        full_name (str): The full name of the recipient.
        email (str): The email address of the recipient.
        phone (str): The phone number of the recipient.
        address (str): The street address of the recipient.
        city (str): The city of the recipient.
        country (str): The country of the recipient.
        zipcode (int): The postal code of the recipient.

    Methods:
        __str__():
            Returns a string representation of the shipping details.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shipping_addresses"
    )
    full_name = models.CharField(max_length=1000)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=1000, null=True)
    city = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    zipcode = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.full_name}'s shipping details"


DELIVERY_STATUS_CHOICES = (
    ("PENDING", "PENDING"),
    ("PACKING", "PACKING"),
    ("SHIPPING", "SHIPPING"),
    ("ARRIVING", "ARRIVING"),
    ("SUCCESS", "SUCCESS"),
)

PAYMENT_STATUS_CHOICES = (
    ("PENDING", "PENDING"),
    ("PROCESSING", "PROCESSING"),
    ("SUCCESSFUL", "SUCCESSFUL"),
    ("CANCELLED", "CANCELLED"),
    ("FAILED", "FAILED"),
)


class Order(BaseModel):
    """
    Represents a customer's order.

    Attributes:
        user (ForeignKey): The user who placed the order.
        tx_ref (str): The unique transaction reference.
        delivery_status (str): The delivery status of the order.
        payment_status (str): The payment status of the order.

    Methods:
        __str__():
            Returns a string representation of the transaction reference.
        save(*args, **kwargs):
            Overrides the save method to generate a unique transaction reference when a new order is created.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    tx_ref = models.CharField(max_length=100, blank=True, unique=True)
    delivery_status = models.CharField(
        max_length=20, default="PENDING", choices=DELIVERY_STATUS_CHOICES
    )
    payment_status = models.CharField(
        max_length=20, default="PENDING", choices=PAYMENT_STATUS_CHOICES
    )

    date_delivered = models.DateTimeField(null=True, blank=True)

    # Shipping address details
    full_name = models.CharField(max_length=1000, null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=1000, null=True)
    city = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=100, null=True)
    zipcode = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.user.full_name}'s order"


    def save(self, *args, **kwargs) -> None:
        if self._state.adding:
            self.tx_ref = generate_unique_code(Order, "tx_ref")
        super().save(*args, **kwargs)

    @property
    def get_cart_subtotal(self):
        orderitems = self.orderitems.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_total(self):
        total = self.get_cart_subtotal
        return total

class OrderItem(BaseModel):
    """
    Represents an item within an order.

    Attributes:
        order (ForeignKey): The order to which this item belongs.
        product (ForeignKey): The product associated with this order item.
        quantity (int): The quantity of the product ordered.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(
        Order,
        related_name="orderitems",
        null=True,
        on_delete=models.CASCADE,
        blank=True,
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def get_total(self):
        return self.product.price_current * self.quantity

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.product.name)
