from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Manufacturer, Product, Order

# Create your views here.
def index(req):
  products = Product.manager.all()
  orders = Order.manager.all()
  print orders

  #print orders[0].products.all()
  
  context = {
    'products': products,
    'orders': orders
  }
  return render(req, 'inventory/index.html', context)

def render_manufact(req):
  return render(req, 'inventory/manufacturer.html')

def render_product(req):
  manufacturers = Manufacturer.objects.all()
  context = {
    'manufacturers': manufacturers
  }
  return render(req, 'inventory/product.html', context)

def create_manu(req):
  result = Manufacturer.manager.makeManuFacturer(req.POST)

  if result[0] == True:
    return redirect('/new/products')

  for key, message in result[1].iteritems():
    messages.error(req, message)
  return redirect('/new/manufacturer')

def create_product(req):
  result = Product.manager.makeProduct(req.POST)

  if result[0] == True:
    return redirect('/')

  for key, message in result[1].iteritems():
    messages.error(req, message)

  return redirect('/new/products')

def create_order(req):
  result = Order.manager.makeOrder(req.POST)

  if result[0] == True:
    return redirect('/')

  for key, message in result[1].iteritems():
    messages.error(req, message)
  
  return redirect('/')