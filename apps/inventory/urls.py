from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^new/manufacturer$', views.render_manufact),
    url(r'^new/products$', views.render_product),
    url(r'^manufacturer$', views.create_manu),
    url(r'^products$', views.create_product),
    url(r'^orders$', views.create_order),
]