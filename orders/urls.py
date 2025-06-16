from django.urls import path
from . import views

urlpatterns = [
    path('order', views.create_order_view, name='create-order')
]
