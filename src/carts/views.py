from django.shortcuts import render, redirect
from orders.models import Order
from .models import Cart
from products.models import Product
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
        return redirect("cart:home")

    user = request.user
    billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()
    guest_email_id = request.session.get('guest_email_id')
    if user.is_authenticated():
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
    elif guest_email_id is not None:
        guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)
    else:
        pass

    if billing_profile is not None:
        order_obj = Order.objects.new_or_get(billing_profile,cart_obj)

    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form
    }
    return render(request, "carts/checkout.html", context)






