from management.models import Product
import razorpay
from django.shortcuts import redirect, render, HttpResponse
from . models import Address, BookingInfo, Product, Order, Coupon
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt, csrf_protect 



def home(request):
    if request.method == "GET":
        return render(request, "home.html")
    else:

        return redirect("search")


def search(request):

    if request.method == "GET":
        try:
            startdate = request.GET.get("startdate")
  
         
            enddate = request.GET.get("enddate")
            NumberOfDays = request.GET.get("NumberOfDays")
            city = request.GET.get("city")
            NumberOfDays = NumberOfDays
            obj, created = BookingInfo.objects.get_or_create(
                user=request.user, startdate=startdate, enddate=enddate, NumberOfDays=NumberOfDays, city=city)
            products = Product.objects.all()
            return render(request, "search.html", {"products": products, "context": obj})
        except ObjectDoesNotExist:
            products = Product.objects.all()
            return render(request, "search.html", {"products": products})
    else:
        p_slug = request.POST.get("product_slug")
        binfo = BookingInfo.objects.latest('user')
        obj = Order.objects.create(
            user=request.user, product=Product.objects.get(slug=p_slug), bookinginfo=binfo)
        return redirect("order_checkout")


def order_checkout(request):
    if request.method == "GET":

        return render(request, "order_checkout.html")

    if request.method == "POST":
        order = Order.objects.latest('user')
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zipcode = request.POST.get("zipcode")
        print(address)
        address, created = Address.objects.get_or_create(user=request.user,
        address=address,
        city=city,
        state=state,
        zipcode=zipcode)
        order.delivery_address = address
        order.save()
        return redirect("order_summery")


def verify_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("order_summery")


def get_coupon(request):
    code = request.POST.get("couponcode")
    try:
        order = Order.objects.latest('user')
        order.coupon = verify_coupon(request, code)
        order.save()
        messages.success(request, "Successfully added coupon")
        return redirect("order_summery")
    except ObjectDoesNotExist:
        messages.info(request, "You do not have an active order")
        return redirect("")


keyid = 'rzp_test_nGR29AWDgH85E2'
keySecret = 'dGLzzG11Xbrg8xiLJuq4UF5B'
razorpay_client = razorpay.Client(auth=(keyid, keySecret))


def order_summery(request):
     try:
        order = Order.objects.latest('user')
        order.amount = order.product.CostPerDay*order.bookinginfo.NumberOfDays
        if order.coupon:
            order.amount = order.amount-order.coupon.discount_price
            order.save()
        order_currency = 'INR'
        notes = {'order-type': "basic order from the website", 'key': 'value'}
        if order.product.In_inventory:
            razorpay_order = razorpay_client.order.create(dict(
            amount=order.amount*100, currency=order_currency, notes=notes, receipt=order.order_id, payment_capture='1'))
            order.razorpay_order_id = razorpay_order['id']
            order.product.Inventory-=1
            order.save()
            return render(request, 'order_summery.html', {'order': order, 'order_id': razorpay_order['id'], 'orderId': order.order_id, 'razorpay_merchant_id': keyid, })
        else:
            messages.info(request, "Your car is sold out")
            return render("/search")
     except ObjectDoesNotExist:
            messages.info(request, "You do not have an active order")
            return redirect("")


@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
             a = (request.POST)
             order_id = ""
             data = {}
             for key, val in a.items():
                if key == "razorpay_order_id":
                    data["razorpay_order_id"] = val
                elif key == "razorpay_payment_id":
                    data["razorpay_payment_id"] = val
                elif key == "razorpay_signature":
                    data["razorpay_signature"] = val
             print(data)
             try:
                 obj=Order.objects.filter(razorpay_order_id=data["razorpay_order_id"]).first()
                 client=razorpay.Client(auth=(keyid, keySecret))
                 check=client.utility.verify_payment_signature(data)
                 print(check)
                 if check==None:
                    obj.status="paid"
                    print(obj.status)
                    obj.razorpay_payment_id=data["razorpay_payment_id"]
                    obj.razorpay_signature=data["razorpay_signature"]
                    obj.save()
             except ObjectDoesNotExist:
                messages.info(request, "Payment not successful")
                redirect("order_summery")


    return redirect("/")

def profile_view(request):
    return render(request, 'account/profile.html')


    
