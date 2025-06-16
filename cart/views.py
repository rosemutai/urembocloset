from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from  store.models import Product
from .shoppingcart import Cart
from .forms import CartAddProductForm

# Create your views here.
@require_POST
def add_product_to_cart_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product = product,
            quantity = cd['quantity'],
            override_quantity = cd['override']
        )
    return redirect('cart-detail')

@require_POST
def remove_product_from_cart_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart-detail')

def cart_detail_view(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial = {'quantity': item['quantity'], 'override': True}
        )
    return render(request, 'cart/cart-detail.html', {'cart': cart})


def order_completed_view(request):
    return render(request, 'cart/order-completed.html')
