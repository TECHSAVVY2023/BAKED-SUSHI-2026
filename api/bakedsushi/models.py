from django.db import models
from django.template import defaultfilters


class ContactListModel(models.Model):
    contact_id = models.CharField(max_length=255, blank=True, null=True, default='')
    firstname = models.CharField(max_length=255, blank=True, null=True, default='')
    lastname = models.CharField(max_length=255, blank=True, null=True, default='')
    contact_email = models.CharField(max_length=255, blank=True, null=True, default='')
    contact_number = models.CharField(max_length=255, blank=True, null=True, default='')
    message = models.CharField(max_length=500, blank=True, null=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def created_at_formatted(self):
        return defaultfilters.date(self.created_at, 'M d, Y')


class Product(models.Model):
    """A menu item / product sold by Baked Sushi."""
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)  # stored in Philippine Pesos (whole number)
    description = models.TextField(blank=True, default='')
    available = models.BooleanField(default=True)
    image_url = models.CharField(max_length=1000, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name


class Order(models.Model):
    """A customer order placed with Baked Sushi."""
    customer = models.CharField(max_length=255)
    total = models.IntegerField(default=0)   # stored in Philippine Pesos (whole number)
    items = models.IntegerField(default=1)   # number of line items in the order
    paid = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'Order #{self.pk} — {self.customer}'