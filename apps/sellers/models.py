from autoslug import AutoSlugField
from django.db import models

from apps.accounts.models import User
from apps.common.models import BaseModel


class Seller(BaseModel):
    # Link to the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="seller")

    # Business Information
    business_name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="business_name", always_update=True, null=True)
    inn_identification_number = models.CharField(max_length=50)
    website_url = models.URLField(null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    business_description = models.TextField()

    # Address Information
    business_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    # Bank Information
    bank_name = models.CharField(max_length=255)
    bank_bic_number = models.IntegerField()
    bank_account_number = models.CharField(max_length=50)
    bank_routing_number = models.CharField(max_length=50)

    # Status fields
    is_approved = models.BooleanField(default=False)


    def __str__(self):
        return f"Seller for {self.business_name}"
