from django.contrib import admin
from .models import UserProfile,Product,BookingInfo,Address,Order,Coupon
admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(BookingInfo)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Coupon)