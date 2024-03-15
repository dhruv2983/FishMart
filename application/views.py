from django.shortcuts import render, redirect
from .forms import UserSignUpForm
from django.contrib.auth import login, authenticate, logout
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404


def index(request):
    context = {"shop_owner": request.user.is_authenticated and request.user.is_seller}
    return render(request, "index.html", context)


def signup(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = UserSignUpForm()
    return render(request, "signup.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
    return redirect(request.META.get("HTTP_REFERER", "/"))


def logout_user(request):
    logout(request)
    return redirect("/")


@login_required
def view_products(request):
    products = Product.objects.all()
    return render(request, "products.html", {"products": products})


@login_required
@require_http_methods(["POST"])
def order(request):
    product_id = request.POST.get("product_id")
    product = Product.objects.get(id=product_id)
    quantity = request.POST.get("quantity")
    address = request.POST.get("address")
    payment_method = request.POST.get("paymentRadio")
    delivery_method = request.POST.get("deliveryRadio")
    card_number = request.POST.get("cardNumber", "")
    expiry_date = request.POST.get("expiryDate", None)
    cvv = request.POST.get("cvv", "")

    print(payment_method)

    order = Order(
        product=product,
        quantity=quantity,
        address=address,
        payment_method=payment_method,
        card_number=card_number if payment_method == "card" else "",
        expiry_date=expiry_date if payment_method == "card" else None,
        cvv=cvv if payment_method == "card" else "",
        buyer=request.user,
        delivery_method=delivery_method,
    )
    order.save()

    return render(request, "order.html", {"order": order})


@login_required
def seller(request):
    if not request.user.is_seller:
        return redirect("/")
    products = Product.objects.filter(seller=request.user)
    return render(request, "seller.html", {"products": products})


@login_required
@require_http_methods(["POST"])
def add_product(request):
    name = request.POST.get("product_name")
    price = request.POST.get("product_price")
    description = request.POST.get("product_description")
    Product.objects.create(
        seller=request.user, name=name, price=price, description=description
    )
    return redirect("/seller_products/")


@login_required
@require_http_methods(["POST"])
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    if request.method == "POST":
        product.name = request.POST.get("product_name")
        product.price = request.POST.get("product_price")
        product.description = request.POST.get("product_description")
        product.save()

    return redirect("/seller_products/")


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    product.delete()
    return redirect("/seller_products/")

@login_required
def seller_orders(request):
    if not request.user.is_seller:
        return redirect("/")
    products = Product.objects.filter(seller=request.user)
    orders = Order.objects.filter(product__in=products)
    return render(request, "seller_orders.html", {"orders": orders})