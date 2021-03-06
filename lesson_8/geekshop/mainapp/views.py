import random
from django.shortcuts import render

from mainapp.models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page, never_cache
from django.db.models import F, Q


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


# @never_cache
def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]


def get_some_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk).select_related(
        'category')[:3]
    return same_products


def product(request, pk):
    links_menu = get_links_menu()
    context = {
        'product': get_object_or_404(Product, pk=pk),
        'links_menu': links_menu
    }
    return render(request, 'mainapp/product.html', context)


def index(request):
    is_home = Q(category__name='??????')
    is_office = Q(category__name='????????')
    context = {
        'title': '??????????????',
        'products': Product.objects.filter(
            is_home | is_office
        ),
    }
    return render(request, 'mainapp/index.html', context)


def contact(request):
    context = {
        'title': '????????????????'
    }
    return render(request, 'mainapp/contact.html', context)


@cache_page(3600)
def products(request, pk=None, page=1):
    links_menu = get_links_menu()
    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category_item = {
                'name': '??????',
                'pk': 0
            }
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk)

        # page = request.GET.get('p', 1) => ???????????? "page = 1"
        paginator = Paginator(products_list, 3)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'links_menu': links_menu,
            'title': '????????????????',
            'category': category_item,
            'products': products_paginator
        }
        return render(request, 'mainapp/products_list.html', context=context)

    hot_product = get_hot_product()
    same_products = get_some_products(hot_product)
    context = {
        'links_menu': links_menu,
        'title': '????????????????',
        'hot_product': hot_product,
        'same_products': same_products,
    }
    return render(request, 'mainapp/products.html', context=context)
