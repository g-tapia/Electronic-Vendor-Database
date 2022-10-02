from django.db import models
from django.db.models.constraints import *
from product.models import Product
from warehouseStore.models import Store, Warehouse

# Create your models here.
class Member(models.Model):
    m_id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.CharField(unique=True, max_length=50, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    user_status = models.IntegerField(blank=True, null=True)
    reg_date = models.DateField()
    billing_date = models.DateField(blank=True, null=True)

    def get_name(self):
        return self.name
    
    class Meta:
        managed = False
        db_table = 'member'

class storeAdmin(models.Model):
    store_a_id = models.CharField(primary_key=True, max_length=50)
    s = models.ForeignKey(Store, models.DO_NOTHING, null=False, db_column='s_id')
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.CharField(unique=True, max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'storeAdmin'

class warehouseAdmin(models.Model):
    wh_a_id = models.CharField(primary_key=True, max_length=50)
    w = models.ForeignKey(Warehouse, models.DO_NOTHING, null=False, db_column='w_id')
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.CharField(unique=True, max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'warehouseAdmin'

class Bank(models.Model):
    card_num = models.ForeignKey('Membercardinfo', models.DO_NOTHING, db_column='card_num', blank=True, null=True)
    balance = models.FloatField()

    class Meta:
        managed = False
        db_table = 'bank'

class Memberaddress(models.Model):
    id = models.AutoField(primary_key=True)
    m = models.ForeignKey(Member, models.DO_NOTHING, blank=True, null=True)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=15)
    
    class Meta:
        managed = False
        db_table = 'memberAddress'
        unique_together = ('m', 'address1')

class Membercardinfo(models.Model):
    id = models.AutoField(primary_key=True)
    m = models.ForeignKey(Member, models.DO_NOTHING, blank = False, null = True)
    card_num = models.CharField(unique=True, max_length=20)
    card_name = models.CharField(max_length=30)
    card_exp_month = models.IntegerField(blank=False, null=True)
    card_exp_year = models.IntegerField(blank=False, null=True)
    balance = models.FloatField()

    class Meta:
        managed = False
        db_table = 'memberCardInfo'
        unique_together = ('m', 'card_num')

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    m = models.ForeignKey(Member, models.DO_NOTHING)
    p = models.ForeignKey('product.Product', models.DO_NOTHING)
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cart'
        unique_together = (('m', 'p'),)