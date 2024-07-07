from django.shortcuts import render, get_object_or_404
from .models import Category,Product
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug = category_slug)
        products = products.filter(category=category)

    paginator = Paginator(products, 7) 
    page = request.GET.get('page')

    try: 
        products_paginated = paginator.page(page)
    except PageNotAnInteger:
        products_paginated = paginator.page(1)
    except EmptyPage:
        products_paginated = paginator.page(paginator.num_pages)

    return render(request, "shop/product_list.html", {
        "category": category,
        "categories": categories,
        "products": products,
        "products_paginated": products_paginated
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, "shop/product_detail.html", {
        "product": product,
        "cart_product_form": cart_product_form,
    })