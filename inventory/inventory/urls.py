"""inventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$',"logistics.views.home",name="home"),
    url(r'^products/available/$',"logistics.views.availableProducts",name="availableProducts"),
    url(r'^products/add/$',"logistics.views.addProduct",name="addProduct"),
    url(r'^products/supply/$',"logistics.views.supplyProducts",name="supplyProducts"),
    url(r'^products/supply/confirmation/$',"logistics.views.supplyProductConfirmation",name="supplyProductConfirmation"),
    url(r'^products/add/confirmation/$',"logistics.views.addProductConfirmation",name="addProductConfirmation"),
    url(r'^product/invalid/$',"logistics.views.invalidProduct",name="invalidProduct"),
    url(r'^product/(?P<name>[a-z0-9A-Z]+)/(?P<brand>[a-z0-9A-Z]+)/(?P<weight>[0-9]+)/$',"logistics.views.productInfo",name="productInfo"),
    url(r'^customer/add/$',"logistics.views.addCustomer",name="addCustomer"),
    url(r'^customer/invalid/$',"logistics.views.invalidCustomer",name="invalidCustomer"),
    url(r'^customer/add/confirmation/$',"logistics.views.addCustomerConfirmation",name="addCustomerConfirmation"),
    url(r'^customer/transactions/$',"logistics.views.customerTransactions",name="customerTransactions"),
    url(r'^customer/transactions/error/$',"logistics.views.customerTransactionsError",name="customerTransactionsError"),
    url(r'^supplier/add/$',"logistics.views.addSupplier",name="addSupplier"),
    url(r'^supplier/invalid/$',"logistics.views.invalidSupplier",name="invalidSupplier"),
    url(r'^supplier/add/confirmation/$',"logistics.views.addSupplierConfirmation",name="addSupplierConfirmation"),
    url(r'^supplier/transactions/$',"logistics.views.supplierTransactions",name="supplierTransactions"),
    url(r'^supplier/transactions/error/$',"logistics.views.supplierTransactionsError",name="supplierTransactionsError"),
    url(r'^receive/money/details/$',"logistics.views.payDetails",name="payDetails"),
    url(r'^receive/money/error/$',"logistics.views.payDetailsError",name="payDetailsError"),
    url(r'^receive/money/confirmation/$',"logistics.views.payDetailsConfirmation",name="payDetailsConfirmation"),
    url(r'^send/money/$',"logistics.views.sendMoney",name="sendMoney"),
    url(r'^send/money/error/$',"logistics.views.sendMoneyError",name="sendMoneyError"),
    url(r'^send/money/confirmation/$',"logistics.views.sendMoneyConfirmation",name="sendMoneyConfirmation"),
    url(r'^miscellaneous/expenditure/$',"logistics.views.miscellaneousExpenditure",name="miscellaneousExpenditure"),
    url(r'^miscellaneous/expenditure/confirmation/$',"logistics.views.miscellaneousExpenditureConfirmation",name="miscellaneousExpenditureConfirmation"),
    url(r'^summary/day/$',"logistics.views.dayWiseSummary",name="dayWiseSummary"),
    url(r'^summary/month/$',"logistics.views.monthWiseSummary",name="monthWiseSummary"),
    url(r'^summary/overall/$',"logistics.views.overallSummary",name="overallSummary"),
    url(r'^admin/', include(admin.site.urls)),
]
