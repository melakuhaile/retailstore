from __future__ import unicode_literals

from django.db import models

def uni_str_dict(mydict):
  data = {}
  for key, val in mydict.iteritems():
    if key != 'csrfmiddlewaretoken':
      data[key] = str(val)
  return data


#Create your managers here.
class ManufacturerMangager(models.Manager):
  def makeManuFacturer(self, form):
    flag = False
    errors = {}
    data = uni_str_dict(form)

    if len(data['name']) < 3:
      errors['name'] = 'Name must be longer than three characters' 
      flag = True

    
    if flag:
      return (False, errors)

    manu = self.create(name=data['name'], email=data['email'], manufacturer_id=data['manufacturer_id'], location=data['location'])

    return (True, manu)

class ProductManager(models.Manager):
  def makeProduct(self, form): 
    flag = False
    errors = {}
    data = uni_str_dict(form)

    if data['unit_price'] < 0:
      flag = True
      errors['unit_price'] = 'Unit price must be 0 or more dollars'
    
    if data ['retail_price'] <= data['unit_price']:
      flag = True
      errors['retial_price'] = 'Retail price must be greater than unit price'
    
    if flag:
      return (False, errors)

    product = self.create( name=data['name'], unit_price=data['unit_price'], retail_price=data['retail_price'], stock=data['stock'], manufacturer=Manufacturer.objects.get(id=data['manufacturer']))
    return (True, product)
    
class OrderManager(models.Manager):
  def makeOrder(self, form):
    flag = False
    errors = {}
    data = uni_str_dict(form)

    if data['product_1'] == '':
      flag = True
      errors['product_1'] = 'Fill in Product 1 Field'
    
    if data['product_2'] == '':
      flag = True
      errors['product_2'] = 'Fill in Product 2 Field'
    
    if data['product_3'] == '':
      flag = True
      errors['product_3'] = 'Fill in Product 3 Field'

    if flag:
      return (False, errors)

    product_1 = Product.manager.get(id=data['product_1'])
    product_2 = Product.manager.get(id=data['product_2'])
    product_3 = Product.manager.get(id=data['product_3'])

    total = product_1.retail_price + product_2.retail_price + product_3.retail_price

    order = self.create(total=total, username=data['username'])

    order.products.add(product_1)
    order.products.add(product_2)
    order.products.add(product_3)

    order.save()

    return (True, order)

# Create your models here.
class Manufacturer(models.Model):
  name = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  manufacturer_id = models.IntegerField()
  location = models.CharField(max_length=255)
  manager = ManufacturerMangager()
  objects = models.Manager() 

class Product(models.Model):
  name = models.CharField(max_length=255)
  unit_price = models.FloatField()
  retail_price = models.FloatField()
  stock = models.IntegerField()
  manufacturer = models.ForeignKey(Manufacturer, related_name="products")
  manager = ProductManager()

class Order(models.Model):
  username = models.CharField(max_length=255)
  total = models.FloatField()
  products = models.ManyToManyField(Product, related_name='orders')
  manager = OrderManager()
