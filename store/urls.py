from django.urls import path
from store import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list_view, name='products'),
    # path('products/<str:slug>/', views.product_list_view, name='products-by-category'),
    path('product-details/<int:id>/<slug:slug>/', views.product_details_view, name='product-details'),
    path('add-product', views.add_product_view, name='add-product'),
    path('edit-product/<int:id>/', views.edit_product_view, name='edit-product'),
    path('delete-product/<int:id>/', views.delete_product_view, name='delete-product'),
    path('success', views.success, name='success'),
]
