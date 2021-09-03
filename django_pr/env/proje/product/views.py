from django.shortcuts import render, render_to_response
from .models import Product
from django.http import request

def index(request):
    products = Product.objects.all()
    return render_to_response("product/index.html", {"products":products})