from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

def main(request):
    product_list = Product.objects.order_by('p_id')
    context = { 'product_list': product_list}
    return render(request,'product_list.html', context)
    

def product_detail(request):
    render(request)