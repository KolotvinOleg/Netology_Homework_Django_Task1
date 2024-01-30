from django.shortcuts import render, redirect, get_object_or_404
from .models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    phones = Phone.objects.all()
    if request.GET.get('sort') == 'name':
        phones = Phone.objects.order_by('name')
    elif request.GET.get('sort') == 'min_price':
        phones = Phone.objects.order_by('price')
    elif request.GET.get('sort') == 'max_price':
        phones = Phone.objects.order_by('-price')
    context = {
        'phones': phones
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = get_object_or_404(Phone, slug=slug)
    context = {'phone': phone}
    return render(request, template, context)
