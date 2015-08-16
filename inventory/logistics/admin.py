from django.contrib import admin
from .forms import CustomerForm,ProductForm,SupplierForm, MiscellaneousExpenditureForm
from .models import Product,Customer,MoneyReceivedInformation,SupplyProductsInformation,Supplier, MoneyPaidInformation, MiscellaneousExpenditureInformation
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
admin.site.register(Product, ProductAdmin)

class CustomerAdmin(admin.ModelAdmin):
    form = CustomerForm
admin.site.register(Customer, CustomerAdmin)

class SupplierAdmin(admin.ModelAdmin):
    form = SupplierForm
admin.site.register(Supplier, SupplierAdmin)

class MiscellaneousExpenditureAdmin(admin.ModelAdmin):
    form = MiscellaneousExpenditureForm
admin.site.register(MiscellaneousExpenditureInformation, MiscellaneousExpenditureAdmin)

admin.site.register(MoneyReceivedInformation)
admin.site.register(MoneyPaidInformation)


admin.site.register(SupplyProductsInformation)