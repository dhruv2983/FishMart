from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("signup/", signup, name="signup"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("products/", view_products, name="products"),
    path("order/", order, name="order"),
    path("add_product/", add_product, name="add_product"),
    path("edit_product/<int:product_id>", edit_product, name="edit_product"),
    path("delete_product/<int:product_id>", delete_product, name="delete_product"),
    path("seller_products/", seller, name="seller"),
    path("seller_orders/", seller_orders, name="seller_orders"),
]
