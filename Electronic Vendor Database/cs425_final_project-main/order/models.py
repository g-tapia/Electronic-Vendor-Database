from django.db import models
from user.models import Member
from product.models import Product, Shippingcompany, Manufacturer
from warehouseStore.models import Store


class Orderlist(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    order_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'orderList'
        

class Onlineorder(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Orderlist', models.DO_NOTHING)
    order_date = models.DateField()
    p = models.ForeignKey('product.Product', models.DO_NOTHING, blank=True, null=True)
    quantity = models.IntegerField()
    customer_type = models.IntegerField(blank=True, null=True)
    m = models.ForeignKey(Member, models.DO_NOTHING, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    card_info = models.CharField(max_length=20)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=15)
    phone_num = models.BigIntegerField()
    recipient_name = models.CharField(max_length=30)
    recipient_phone = models.BigIntegerField()
    sc = models.ForeignKey(Shippingcompany, models.DO_NOTHING, blank=True, null=True)
    tracking_num = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'onlineOrder'


class Instoreorder(models.Model):
    order = models.ForeignKey('Orderlist', models.DO_NOTHING)
    s = models.ForeignKey('warehouseStore.Store', models.DO_NOTHING, blank=True, null=True)
    p = models.ForeignKey('product.Product', models.DO_NOTHING, blank=True, null=True)
    quantity = models.IntegerField()
    customer_type = models.IntegerField(blank=True, null=True)
    m = models.ForeignKey('user.Member', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instoreOrder'
