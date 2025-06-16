from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseForbidden
from decimal import Decimal
from django.db.models import Count

from user.models import User
from store.models import Category, Product, Review, ProductImage
from cart.forms import CartAddProductForm

# Create your views here.
# categories: women men kids shoes
def index(request):
    return render(request, 'store/index.html')

def product_list_view(request):
    products = Product.objects.filter(is_active=True)
    paginator = Paginator(products, 10)

    num_of_products = request.GET.get('products-num')
    if num_of_products:
        paginator = Paginator(products, num_of_products)

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)


    for product in page_obj:
        if product.discount > 0:
            product.new_price = product.price * (1 - (product.discount / Decimal(100)))
            
        else:
            product.new_price = product.price

    return render(request, 'store/products.html', {
        'page_obj': page_obj
    })

def product_details_view(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, is_active=True)
    cart_product_form = CartAddProductForm()

    product_rating_count = Review.objects.filter(product=product).count()
    images = ProductImage.objects.filter(product=product)

    return render(request, 'store/product-details.html', {
        'product': product,
        'product_rating_count': product_rating_count,
        'images': images,
        'cart_product_form': cart_product_form
    })

def add_product_view(request):

    categories = Category.objects.all()

    if request.user.role != 'admin':
        return HttpResponseForbidden('You do not have permissions to perform this action')
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        discount = request.POST['discount']
        category_id = request.POST['category']
        category = Category.objects.get(id=category_id)
        stock_quantity = request.POST['stock-quantity']
        featured_image = request.FILES['featured-image']
        SKU = request.POST['SKU']
        other_product_images = request.FILES.getlist('multiple-images')

        product = Product.objects.create(
            name = name,
            description = description,
            price = price,
            discount = discount,
            category = category,
            stock_quantity = stock_quantity,
            featured_image = featured_image,
            SKU = SKU
        )

        for image in other_product_images:
            ProductImage.objects.create(
                product=product,
                image = image
            )

        return redirect('products')
    return render(request, 'store/add-products.html', {
        'categories': categories
    })

def edit_product_view(request, id):
    product = get_object_or_404(Product, id=id)
    current_images = ProductImage.objects.filter(product=product)
    categories = Category.objects.all()

    if request.user.role != 'admin':
        return HttpResponseForbidden('You do not have permissions to perform this action')
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        discount = request.POST.get('discount')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        stock_quantity = request.POST.get('stock-quantity')
        SKU = request.POST.get('SKU')
        new_images = request.FILES.getlist('multiple-images')
        delete_image_ids = request.POST.getlist('delete-images')
    
        product.name = name
        product.description = description
        product.price = price
        product.discount = discount
        product.category = category
        product.stock_quantity = stock_quantity
        if 'featured-image' in request.FILES:
            product.featured_image = request.FILES['featured-image']
        product.save()

        ProductImage.objects.filter(id__in=delete_image_ids, product=product).delete()

        for image in new_images:
            ProductImage.objects.create(product=product, image=image)

        return redirect('product-details', id=product.id)

    return render(request, 'store/edit-product.html', {
        'product': product,
        'categories': categories,
        'current_images': current_images
    })

def success(request):
    return render(request, 'store/success.html')

def delete_product_view(request, id):
    product = get_object_or_404(Product, id=id)
    if request.user.role != 'admin':
        return HttpResponseForbidden('You do not have permissions to perform this action')
    
    if request.method == 'POST':
        product.is_active = False
        product.save()
        url = reverse('products')
        return redirect(f'{url}?deleted={product.name}')