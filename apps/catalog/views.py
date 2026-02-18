from django.shortcuts import render
from .models import Product

def home(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'catalog/home.html', {'products': products})
