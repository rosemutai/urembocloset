from django.urls import path
from . import views

urlpatterns = [
    path('cart-detail', views.cart_detail_view, name='cart-detail'),
    path('add-to-cart/<int:product_id>/', views.add_product_to_cart_view, name='add-to-cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_product_from_cart_view, name='remove_from-cart'),
]
