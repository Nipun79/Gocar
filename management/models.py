from django.db.models.lookups import EndsWith
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.shortcuts import redirect
from django.utils import timezone


CATEGORY_CHOICES = (
    ("Premium", "Premium"),
    ("Luxury", "Luxury"),
    ("Economical", "Economical"),
)

LABEL_CHOICES = (
    ("Manual", "Manual"),
    ("Automatic", "Automatic")
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

STATUS_CHOICES = (
    ('created', 'created'),
    ('paid', 'paid'),
    ('delivered', 'delivered'),
    ('returned', 'returned'),
    ('refunded', 'refunded')
)
FUEL_TYPE_CHOICES=(
    ('Petrol','Petrol'),
    ('Diesel','Diesel'),
    ('Electric','Electric')
)

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Product(models.Model):
    Name = models.CharField(max_length=100)
    CostPerDay = models.FloatField(default=0)
    category = models.CharField(
        choices=CATEGORY_CHOICES, max_length=50, default="Premium")
    label = models.CharField(choices=LABEL_CHOICES,
                             max_length=50, default="Manual")
    fuel_type=models.CharField(choices=FUEL_TYPE_CHOICES, max_length=50,default="Petrol")
    seats=models.IntegerField(default=2)
    slug = models.SlugField()
    image = models.ImageField(upload_to="images/")
    Inventory=models.IntegerField(default=1)
    In_inventory=models.BooleanField(default=True)
    def __str__(self):
        return self.Name
    


class BookingInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    startdate = models.DateField()
    enddate = models.DateField()
    city = models.CharField(max_length=50, default="Hyderabad")
    NumberOfDays = models.FloatField(default=0)
class Coupon(models.Model):
    code=models.CharField(max_length=20, null=False,blank=True)
    discount_price=models.IntegerField(default=0)
    def __str__(self):
        return f"CODE= {self.code} , PRICE= {self.discount_price}"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True)
    delivery_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=50, default="created")
    bookinginfo = models.ForeignKey(
        BookingInfo, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField(default=0)
    coupon=models.ForeignKey(Coupon,on_delete=models.SET_NULL, blank=True, null=True)
    datetime_of_payment = models.DateTimeField(default=timezone.now)

     # related to razorpay
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)
    def save(self, *args, **kwargs):
        if self.order_id is None and self.datetime_of_payment and self.id:
            self.order_id = self.datetime_of_payment.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
    def inventory_count(self):
        inventory=self.product.inventory-1
        return inventory


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=False,blank=True)
    city = models.CharField(max_length=200, null=False,blank=True)
    state = models.CharField(max_length=200, null=False,blank=True)
    zipcode = models.CharField(max_length=200, null=False,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)
post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
