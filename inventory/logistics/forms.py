from django import forms
from .models import Customer,Product,Supplier,MiscellaneousExpenditureInformation


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["customer_name","city"]

    def clean(self):
        cleaned_data = super(CustomerForm,self).clean()
        customer_name = cleaned_data.get("customer_name")
        city = cleaned_data.get("city")
        customers = Customer.objects.all()
        if city is not None and customer_name is not None:
            for customer in list(customers) :
                if customer.customer_name.lower() == customer_name.lower() and customer.city.lower() == city.lower():
                    msg = "Customer name you entered is already present in the entered city"
                    self._errors["customer_name"] = self.error_class([msg])
        return self.cleaned_data

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["supplier_name","city"]

    def clean(self):
        cleaned_data = super(SupplierForm,self).clean()
        supplier_name = cleaned_data.get("supplier_name")
        city = cleaned_data.get("city")
        suppliers = Supplier.objects.all()
        if city is not None and supplier_name is not None:
            for supplier in list(suppliers) :
                if supplier.supplier_name.lower() == supplier_name.lower() and supplier.city.lower() == city.lower():
                    msg = "Supplier name you entered is already present in the entered city"
                    self._errors["supplier_name"] = self.error_class([msg])
        return self.cleaned_data

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["product_name","brand","weight","quantity","buying_price","selling_price","transport_price","supplier","supplier_city","loading_date"]

class MiscellaneousExpenditureForm(forms.ModelForm):
    class Meta:
        model = MiscellaneousExpenditureInformation
        fields = ["expenditure_amount","remarks","date"]