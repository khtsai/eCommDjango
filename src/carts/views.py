from django.shortcuts import render, redirect
from orders.models import Order
from .models import Cart
from products.models import Product
from addresses.forms import AddressForm
from addresses.models import Address
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from accounts.models import GuestEmail
# Create your views here.

def cart_create():
    cart_obj = Cart.objects.create(user=None)
    print('create a new cart...')
    return cart_obj

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = cart_obj.products.all()
#     cart_id = request.session.get("cart_id", None)
#     qs = Cart.objects.filter(id=cart_id)
#     if qs.count() == 1:
#         print('cart ID exists...')
#         print(cart_id)
#         cart_obj = qs.first()
#         if request.user.is_authenticated() and cart_obj.user is None:
#             cart_obj.user = request.user
#             cart_obj.save()
#     else:
#         cart_obj = Cart.objects.new(user = request.user)
#         request.session['cart_id']=cart_obj.id
    return render(request, "carts/cart_home.html", {"cart":cart_obj})

def cart_update(request):
    print(request.POST)
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Product is gone....")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
        request.session['cart_items'] = cart_obj.products.count()
        
    return redirect("carts:home")#redirect(product_obj.get_absolute_url())

def checkout_home(request):
    cart_obj, new_cart_obj = Cart.objects.new_or_get(request)
    order_obj = None
    if new_cart_obj:
        return redirect("carts:home")

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    #billing_address_form = AddressForm()
    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    if billing_profile is not None:
        #print(cart_obj) 23
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile,cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if billing_address_id or shipping_address_id:
            order_obj.save()    

    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        #'billing_address_form': billing_address_form
    }
    return render(request, "carts/checkout.html", context)






