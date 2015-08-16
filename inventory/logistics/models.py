from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    weight = models.IntegerField()
    quantity = models.IntegerField()
    buying_price = models.IntegerField()
    selling_price = models.IntegerField()
    transport_price = models.IntegerField()
    supplier = models.CharField(max_length=50)
    supplier_city = models.CharField(max_length=50)
    loading_date = models.DateField(help_text="YYYY-MM-DD")
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('logistics.views.productInfo',args=[self.product_name,self.brand,str(self.weight)] )


class Customer(models.Model):
    customer_name = models.CharField(max_length=30)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.customer_name

class Supplier(models.Model):
    supplier_name = models.CharField(max_length=30)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.supplier_name

class MoneyReceivedInformation(models.Model):
    customer_name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    amount_paid = models.IntegerField()
    remarks = models.CharField(max_length=100,blank=True)
    date = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)

    def __str__(self):
        return self.customer_name

class MoneyPaidInformation(models.Model):
    supplier_name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    amount_paid = models.IntegerField()
    remarks = models.CharField(max_length=100,blank=True)
    date = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)

    def __str__(self):
        return self.supplier_name

class MiscellaneousExpenditureInformation(models.Model):
    expenditure_amount = models.IntegerField()
    remarks = models.CharField(max_length=100)
    date = models.DateField(help_text="YYYY-MM-DD")
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)

    def __str__(self):
        return self.remarks

class SupplyProductsInformation(models.Model):
    customer_name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    product_name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    weight = models.IntegerField()
    selling_price = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateField()
    remarks = models.CharField(max_length=100,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)

    def __str__(self):
        return self.customer_name