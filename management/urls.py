from django.urls import path
from .views import (home,search,order_checkout,order_summery,get_coupon,handlerequest,profile_view)
urlpatterns = [
    path('',home,name="home"),
    path('search/',search,name="search"),
    path("order_checkout/",order_checkout,name="order_checkout"),
    path('get_coupon',get_coupon,name="get_coupon"),
    path('handlerequest', handlerequest, name = 'handlerequest'),
    path('order_summery/',order_summery,name="order_summery"),
    path('accounts/profile/', profile_view, name='account_profile'),
   

]