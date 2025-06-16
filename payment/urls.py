from django.urls import path

from . import views, webhooks

urlpatterns = [
    path('process/', views.process_payment_view, name='process-payment'),
    path('completed/', views.payment_completed_view, name='completed'),
    path('canceled/', views.payment_canceled_view, name='canceled'),
    path('webhook/', webhooks.stripe_webhook, name='stripe-webhook'),
    
]
