"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('cookie', view),
    path('edit/', edit),
    path('history/', history),
    path('checkout/', checkout),
    path('signup/', signup),
    path('login/', login),
    path('logout/', logout),
    path('cart/', cart),
    path('card/', card),
    path('address/new_address', add_address),
    path('card/new_card', add_card),
    path('address/', address),
    path('product/', include('product.urls')),
    path('user/', include('user.urls')),
    path('<str:p_id>/', product_detail, name = 'detail'),
    path("address/<str:address>/delete", address_delete, name = "address_delete"), 
    path("card/<str:card_num>/delete", card_delete, name = "cart_delete"),
    path('cart/<str:p_id>/delete', cart_delete, name = 'cart_delete'),
    path('cart/<str:p_id>/plus', cart_plus, name = 'cart_plus'),
    path('cart/<str:p_id>/minus', cart_minus, name = 'cart_minus'),

]
