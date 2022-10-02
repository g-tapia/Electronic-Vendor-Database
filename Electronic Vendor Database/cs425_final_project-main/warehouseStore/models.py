from django.db import models
from product.models import Product, Manufacturer

class Warehouse(models.Model):
    w_id = models.CharField(primary_key=True, max_length=10)
    address1 = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'warehouse'

class Store(models.Model):
    s_id = models.CharField(primary_key=True, max_length=10)
    address = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'store'


class Warehouseinv(models.Model):
    id = models.AutoField(primary_key=True)
    w = models.ForeignKey(Warehouse, models.DO_NOTHING)
    p = models.ForeignKey(Product, models.DO_NOTHING)
    quantity = models.IntegerField(blank=True, null=True)
    threshold = models.IntegerField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'warehouseINV'
        unique_together = (('w', 'p'),)


class Warehousereorder(models.Model):
    w = models.OneToOneField(Warehouse, models.DO_NOTHING, primary_key=True)
    manufacturer = models.ForeignKey(Manufacturer, models.DO_NOTHING, blank=True, null=True)
    p = models.ForeignKey(Product, models.DO_NOTHING)
    quantity = models.IntegerField(blank=True, null=True)
    reorderdate = models.DateField(db_column='reorderDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'warehouseReorder'
        unique_together = (('w', 'p', 'reorderdate'),)


class Whcoverage(models.Model):
    w = models.OneToOneField(Warehouse, models.DO_NOTHING, primary_key=True)
    state = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'whCoverage'
        unique_together = (('w', 'state'),)


class Whstore(models.Model):
    w = models.OneToOneField(Warehouse, models.DO_NOTHING, primary_key=True)
    s = models.ForeignKey(Store, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'whStore'
        unique_together = (('w', 's'),)
        


class Storeinv(models.Model):
    id = models.AutoField(primary_key=True) 
    s = models.ForeignKey(Store, models.DO_NOTHING)
    p = models.ForeignKey(Product, models.DO_NOTHING)
    quantity = models.IntegerField(blank=True, null=True)
    threshold = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'storeINV'
        unique_together = (('s', 'p'),)


class Storereorder(models.Model):
    s = models.OneToOneField(Store, models.DO_NOTHING, primary_key=True)
    w = models.ForeignKey('Warehouse', models.DO_NOTHING, blank=True, null=True)
    p = models.ForeignKey(Product, models.DO_NOTHING)
    quantity = models.IntegerField(blank=True, null=True)
    reorderdate = models.DateField(db_column='reorderDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'storeReorder'
        unique_together = (('s', 'p', 'reorderdate'),)


class Restockstore(models.Model):
    s = models.ForeignKey('Store', models.DO_NOTHING, blank=True, null=True)
    w = models.ForeignKey('Warehouse', models.DO_NOTHING, blank=True, null=True)
    p = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    quantity = models.BigIntegerField(blank=True, null=True)
    restock_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'restockStore'


class Restockwarehouse(models.Model):
    w = models.ForeignKey('Warehouse', models.DO_NOTHING, blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, models.DO_NOTHING, blank=True, null=True)
    p = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    quantity = models.BigIntegerField(blank=True, null=True)
    restock_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'restockWarehouse'