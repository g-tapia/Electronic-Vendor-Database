from django.db import models

# Create your models here.


class Manufacturer(models.Model):
    manufacturer_id = models.CharField(primary_key=True, max_length=20)
    manufacturer_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=30)
    phone_num = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'manufacturer'

class Category(models.Model):
    category = models.CharField(primary_key=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'category'

class Product(models.Model):
    p_id = models.CharField(primary_key=True, max_length=10)
    category = models.ForeignKey(Category, models.DO_NOTHING, db_column='category')
    p_name = models.CharField(max_length=50)
    wholesale_price = models.FloatField()
    instore_price = models.FloatField()
    manufacturer = models.ForeignKey(Manufacturer, models.DO_NOTHING, blank=True, null=True)


    def get_pname(self):
        return self.p_name    
    
    class Meta:
        managed = False
        db_table = 'product'

class Shippingcompany(models.Model):
    sc_id = models.CharField(primary_key=True, max_length=20)
    sc_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ShippingCompany'

