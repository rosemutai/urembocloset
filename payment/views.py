from decimal import Decimal
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
import stripe
from orders.models import Order

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def process_payment_view(request):
    order_id = request.session['order_id']
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('completed'))
        cancel_url = request.build_absolute_uri(reverse('canceled'))

        # stripe checkout session data
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }

        for item in order.items.all():
            session_data['line_items'].append(
                {
                    'price_data': {
                        'unit_amount': int((item.price / 128) * Decimal('100')),
                        'currency': 'USD',
                        'product_data': {
                            'name': item.product.name,
                        },
                    },
                    'quantity': item.quantity
                }
            )

        session = stripe.checkout.Session.create(**session_data)
        
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', locals())
    
def payment_completed_view(request):
    return render(request, 'payment/completed.html')

def payment_canceled_view(request):
    return render(request, 'payment/canceled.html')