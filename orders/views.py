from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import OrderCreateForm
from .models import OrderItem, Order
from cart.shoppingcart import Cart

# Create your views here.
@login_required
def create_order_view(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid:
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            for item in cart:
                product = item['product']
                quantity = item['quantity']

                base_price = Decimal(product.price)
                discount = Decimal(product.discount or 0)

                if discount > 0:
                    price = base_price * (Decimal('1.0') - discount / 100)
                else:
                    price = base_price

                OrderItem.objects.create(
                    order = order,
                    product = product,
                    quantity = quantity,
                    price = round(price, 2)

                )
                
                if product.stock_quantity >= quantity:
                    product.stock_quantity -= quantity
                    if product.stock_quantity == 0:
                        product.available = False
                    product.save()
                else:
                    raise ValueError("Not enough stock available")
            cart.clear()
            request.session['order_id'] = order.id
            return redirect('process-payment')
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order-create.html', {
            'cart': cart,
            'form': form
        })
    

def order_history(request):
    orders = request.user.orders.filter(paid=True).order_by('-created_at')
    print(orders)