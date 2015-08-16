from django.shortcuts import render, redirect
from  .models import Product,Customer,MoneyReceivedInformation, SupplyProductsInformation, Supplier, MoneyPaidInformation, MiscellaneousExpenditureInformation
from django.db.models import Q
from .forms import CustomerForm,ProductForm, SupplierForm, MiscellaneousExpenditureForm
from django.core.exceptions import ValidationError
# Create your views here.
def home(request):
    context = {

    }
    return render(request,"base.html",context)

# renders list of available unique products based on productName, brand, weight
def availableProducts(request):
    queryset = Product.objects.all()
    product_info = []
    final_list = []
    for instance in list(queryset):
       product_info.append([instance.product_name.lower(),instance.brand.lower(),instance.weight])
    product_info_set = listOfUniqueLists(product_info)
    for product in product_info_set:
        final_list.append(list(Product.objects.filter(Q(product_name__iexact=product[0])&Q(brand__iexact=product[1])&Q(weight__iexact=product[2])))[0])
    context = {
        "final_list":final_list
    }
    return render(request,"availableProducts.html",context)

def addProduct(request):
    title = "Add New Product"
    form = ProductForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        supplier_name = instance.supplier
        supplier_city = instance.supplier_city
        valid_suppliers = Supplier.objects.filter(supplier_name__iexact = supplier_name)
        valid_cities = []
        for valid_supplier in valid_suppliers:
            valid_cities.append(valid_supplier.city)
        valid_cities_lower = [ valid_city.lower() for valid_city in valid_cities]
        valid_cities_unique = list(set(valid_cities_lower))
        if supplier_city.lower() not in valid_cities_unique:
            return redirect("/supplier/invalid/")

        instance.save()
        return redirect("/products/add/confirmation/")
    context ={
        "title": title,
        "form": form
    }
    return render(request,"addProduct.html",context)

def supplyProducts(request):
    customerQueryset = Customer.objects.all()
    customers = []
    cities = []

    for instance in list(customerQueryset):
        customers.append(instance.customer_name)
        cities.append(instance.city)
    customers_lowercase = [customer.lower() for customer in customers]
    customers_unique = list(set(customers_lowercase))
    cities_lowercase = [city.lower() for city in cities]
    cities_unique = list(set(cities_lowercase))

    productQueryset = Product.objects.all()
    productNames = []
    brands = []
    weights = []

    for instance in list(productQueryset):
        productNames.append(instance.product_name)
        brands.append(instance.brand)
        weights.append(instance.weight)
    productNames_lowercase = [productName.lower() for productName in productNames]
    brands_lowercase = [brand.lower() for brand in brands]
    productNames_unique = list(set(productNames_lowercase))
    brands_unique = list(set(brands_lowercase))
    weights_unique = list(set(weights))

    customer_name = request.POST.get("CustomerName")
    city_name = request.POST.get("CityName")
    product_name = request.POST.get("ProductName")
    brand_name = request.POST.get("BrandName")
    weight = request.POST.get("Weight")
    cost_per_unit = request.POST.get("CostPerUnit")
    number_of_units = request.POST.get("Quantity")
    date = request.POST.get("Date")
    remarks = request.POST.get("Remarks")

    if request.method == 'POST':
        valid_customers = Customer.objects.filter(customer_name__iexact = customer_name)
        valid_cities = []
        for valid_customer in valid_customers:
            valid_cities.append(valid_customer.city)
        valid_cities_lower = [ valid_city.lower() for valid_city in valid_cities]
        valid_cities_unique = list(set(valid_cities_lower))
        valid_products = Product.objects.filter(Q(product_name__iexact=product_name)&Q(brand__iexact=brand_name)&Q(weight__iexact=weight))

        if city_name.lower() not in valid_cities_unique:
            return redirect("/customer/invalid/")

        if len(list(valid_products)) <= 0:
            return redirect("/product/invalid/")

        SupplyProductsInformation(customer_name = customer_name, city = city_name, product_name = product_name, brand = brand_name, weight = weight, selling_price = cost_per_unit, quantity = number_of_units, date = date, remarks = remarks).save()
        return redirect("/products/supply/confirmation/")
    context = {
        "customers_unique":customers_unique,
        "cities_unique":cities_unique,
        "productNames_unique":productNames_unique,
        "brands_unique":brands_unique,
        "weights_unique":weights_unique,

    }
    return render(request,"supplyProducts.html",context)

def invalidProduct(request):
    return render(request,"invalidProduct.html",{})

def invalidCustomer(request):
    return render(request,"invalidCustomer.html",{})

def invalidSupplier(request):
    return render(request,"invalidSupplier.html",{})

def supplyProductConfirmation(request):
    return render(request,"supplyProductConfirmation.html",{})

def addProductConfirmation(request):
    return render(request,"addProductConfirmation.html",{})

def productInfo(request,name,brand,weight):
    products = Product.objects.filter(Q(product_name__iexact=name)&Q(brand__iexact=brand)&Q(weight__iexact=weight))
    total_quantity = sumOfAvailableUnits(products)
    context = {
        "product_name": products[0].product_name,
        "brand": products[0].brand,
        "weight":products[0].weight,
        "price":products[0].selling_price,
        "total_quantity":total_quantity
    }
    return render(request,"productInfo.html",context)

def supplierTransactions(request):
    queryset = Supplier.objects.all()
    suppliers = []
    cities = []

    for instance in list(queryset):
        suppliers.append(instance.supplier_name)
        cities.append(instance.city)
    suppliers_lowercase = [supplier.lower() for supplier in suppliers]
    suppliers_unique = list(set(suppliers_lowercase))
    cities_lowercase = [city.lower() for city in cities]
    cities_unique = list(set(cities_lowercase))

    supplier_name = request.POST.get("SupplierName")
    city_name = request.POST.get("CityName")
    noOfReceivedTransactions = request.POST.get("NoOfReceivedTransactions")
    noOfPaidTransactions = request.POST.get("NoOfPaidTransactions")
    context = {
        "suppliers_unique":suppliers_unique,
        "cities_unique":cities_unique,
    }

    if request.method == 'POST':
        valid_suppliers = Supplier.objects.filter(supplier_name__iexact = supplier_name)
        valid_cities = []
        for valid_supplier in valid_suppliers:
            valid_cities.append(valid_supplier.city)
        valid_cities_lower = [ valid_city.lower() for valid_city in valid_cities]
        valid_cities_unique = list(set(valid_cities_lower))
        if city_name.lower() not in valid_cities_unique:
            return redirect("/supplier/transactions/error/")
        receivedProductDetails = Product.objects.filter(Q(supplier__iexact=supplier_name)&Q(supplier_city__iexact = city_name)).order_by('-loading_date')[:noOfReceivedTransactions]
        amountPaidDetails = MoneyPaidInformation.objects.filter(Q(supplier_name__iexact =supplier_name)&Q(city__iexact = city_name)).order_by('-date')[:noOfPaidTransactions]
        balanceAmount = getBalanceAmountOfSupplier(supplier_name,city_name)
        moneyDetailsLabel = True
        productDetailsLabel = True
        context = {
            "supplierName":supplier_name.capitalize(),
            "cityName":city_name.capitalize(),
            "receivedProductDetails":receivedProductDetails,
            "amountPaidDetails":amountPaidDetails,
            "balanceAmount":balanceAmount,
            "moneyDetailsLabel":moneyDetailsLabel,
            "productDetailsLabel":productDetailsLabel
        }

        productDetailStatus = ""
        amountDetailStatus = ""
        if len(list(receivedProductDetails))<=0:
            productDetailStatus = "No product transactions found"
            productDetailsLabel = False
        if len(list(amountPaidDetails))<=0:
            amountDetailStatus = "No paid transactions found"
            moneyDetailsLabel = False

        if len(productDetailStatus) > 0 or len(amountDetailStatus) > 0:
            context = {
                "supplierName":supplier_name.capitalize(),
                "cityName":city_name.capitalize(),
                "receivedProductDetails":receivedProductDetails,
                "amountPaidDetails":amountPaidDetails,
                "productDetailStatus":productDetailStatus,
                "amountDetailStatus":amountDetailStatus,
                "balanceAmount":balanceAmount,
                "moneyDetailsLabel":moneyDetailsLabel,
                "productDetailsLabel":productDetailsLabel
            }

        return render(request,"supplierTransactionsResult.html",context)
    return render(request,"supplierTransactions.html",context)

def customerTransactions(request):
    queryset = Customer.objects.all()
    customers = []
    cities = []
    for instance in list(queryset):
        customers.append(instance.customer_name)
        cities.append(instance.city)
    customers_lowercase = [customer.lower() for customer in customers]
    customers_unique = list(set(customers_lowercase))
    cities_lowercase = [city.lower() for city in cities]
    cities_unique = list(set(cities_lowercase))

    customer_name = request.POST.get("CustomerName")
    city_name = request.POST.get("CityName")
    noOfSuppliedTransactions = request.POST.get("NoOfSuppliedTransactions")
    noOfPaidTransactions = request.POST.get("NoOfPaidTransactions")
    context = {
        "customers_unique":customers_unique,
        "cities_unique":cities_unique,
    }

    if request.method == 'POST':
        valid_customers = Customer.objects.filter(customer_name__iexact = customer_name)
        valid_cities = []
        for valid_customer in valid_customers:
            valid_cities.append(valid_customer.city)
        valid_cities_lower = [ valid_city.lower() for valid_city in valid_cities]
        valid_cities_unique = list(set(valid_cities_lower))
        if city_name.lower() not in valid_cities_unique:
            return redirect("/customer/transactions/error/")
        suppliedProductDetails = SupplyProductsInformation.objects.filter(Q(customer_name__iexact=customer_name)&Q(city__iexact = city_name)).order_by('-date')[:noOfSuppliedTransactions]
        amountPaidDetails = MoneyReceivedInformation.objects.filter(Q(customer_name__iexact =customer_name)&Q(city__iexact = city_name)).order_by('-date')[:noOfPaidTransactions]
        balanceAmount = getBalanceAmountOfCustomer(customer_name,city_name)
        moneyDetailsLabel = True
        productDetailsLabel = True
        context = {
            "customerName":customer_name.capitalize(),
            "cityName":city_name.capitalize(),
            "suppliedProductDetails":suppliedProductDetails,
            "amountPaidDetails":amountPaidDetails,
            "balanceAmount":balanceAmount,
            "moneyDetailsLabel":moneyDetailsLabel,
            "productDetailsLabel":productDetailsLabel
        }

        productDetailStatus = ""
        amountDetailStatus = ""
        if len(list(suppliedProductDetails))<=0:
            productDetailStatus = "No product transactions found"
            productDetailsLabel = False
        if len(list(amountPaidDetails))<=0:
            amountDetailStatus = "No paid transactions found"
            moneyDetailsLabel = False

        if len(productDetailStatus) > 0 or len(amountDetailStatus) > 0:
            context = {
                "customerName":customer_name.capitalize(),
                "cityName":city_name.capitalize(),
                "suppliedProductDetails":suppliedProductDetails,
                "amountPaidDetails":amountPaidDetails,
                "balanceAmount":balanceAmount,
                "moneyDetailsLabel":moneyDetailsLabel,
                "productDetailsLabel":productDetailsLabel,
                "productDetailStatus":productDetailStatus,
                "amountDetailStatus":amountDetailStatus,
            }

        return render(request,"customerTransactionsResult.html",context)
    return render(request,"customerTransactions.html",context)

def addCustomer(request):
    title = "Add New Customer"
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)

        instance.save()
        return redirect("/customer/add/confirmation/")
    context ={
        "title": title,
        "form": form
    }
    return render(request,"addcustomer.html",context)

def addSupplier(request):
    title = "Add New Supplier"
    form = SupplierForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)

        instance.save()
        return redirect("/supplier/add/confirmation/")
    context ={
        "title": title,
        "form": form
    }
    return render(request,"addSupplier.html",context)

def addCustomerConfirmation(request):
    return render(request,"addCustomerConfirmation.html",{})

def addSupplierConfirmation(request):
    return render(request,"addSupplierConfirmation.html",{})

def payDetails(request):
    queryset = Customer.objects.all()
    customers = []
    cities = []

    for instance in list(queryset):
        customers.append(instance.customer_name)
        cities.append(instance.city)
    customers_lowercase = [customer.lower() for customer in customers]
    customers_unique = list(set(customers_lowercase))
    cities_lowercase = [city.lower() for city in cities]
    cities_unique = list(set(cities_lowercase))

    customer_name = request.POST.get("CustomerName")
    city_name = request.POST.get("CityName")
    amount_paid = request.POST.get("Amount")
    date = request.POST.get("Date")
    remarks = request.POST.get("Remarks")
    if request.method == 'POST':
        valid_customers = Customer.objects.filter(customer_name__iexact = customer_name)
        valid_cities = []
        for valid_customer in valid_customers:
            valid_cities.append(valid_customer.city)
        valid_cities_lower = [ valid_city.lower() for valid_city in valid_cities]
        valid_cities_unique = list(set(valid_cities_lower))
        if city_name.lower() in valid_cities_unique:
            MoneyReceivedInformation(customer_name = customer_name, city = city_name, amount_paid = amount_paid, remarks = remarks, date = date).save()
            return redirect("/receive/money/confirmation/")
        else:
            return redirect("/receive/money/error/")

    context = {
        "customers_unique":customers_unique,
        "cities_unique":cities_unique
    }

    return render(request,"paydetails.html",context)

def sendMoney(request):
    queryset = Supplier.objects.all()
    suppliers = []
    cities = []

    for instance in list(queryset):
        suppliers.append(instance.supplier_name)
        cities.append(instance.city)
    suppliers_lowercase = [supplier.lower() for supplier in suppliers]
    suppliers_unique = list(set(suppliers_lowercase))
    cities_lowercase = [city.lower() for city in cities]
    cities_unique = list(set(cities_lowercase))

    supplier_name = request.POST.get("SupplierName")
    city_name = request.POST.get("CityName")
    amount_paid = request.POST.get("Amount")
    date = request.POST.get("Date")
    remarks = request.POST.get("Remarks")
    if request.method == 'POST':
        valid_suppliers = Supplier.objects.filter(supplier_name__iexact = supplier_name)
        valid_cities = []
        for valid_supplier in valid_suppliers:
            valid_cities.append(valid_supplier.city)
        valid_cities_lower = [ valid_city.lower() for valid_city in valid_cities]
        valid_cities_unique = list(set(valid_cities_lower))
        if city_name.lower() in valid_cities_unique:
            MoneyPaidInformation(supplier_name = supplier_name, city = city_name, amount_paid = amount_paid, remarks = remarks, date = date).save()
            return redirect("/send/money/confirmation/")
        else:
            return redirect("/send/money/error/")

    context = {
        "suppliers_unique":suppliers_unique,
        "cities_unique":cities_unique
    }

    return render(request,"sendMoney.html",context)

def miscellaneousExpenditure(request):
    title = "Enter Miscellaneous Expenditure Details"
    form = MiscellaneousExpenditureForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)

        instance.save()
        return redirect("/miscellaneous/expenditure/confirmation/")
    context ={
        "title": title,
        "form": form
    }
    return render(request,"miscellaneousExpenditure.html",context)

def dayWiseSummary(request):

    context = {

    }
    selected_date = request.POST.get("Date")
    if request.method == 'POST':
        supply_product_info = SupplyProductsInformation.objects.filter(date__iexact = selected_date)
        supply_product_info_summary = getSupplyProductsSummary(supply_product_info, selected_date)
        received_product_info = Product.objects.filter(loading_date__iexact=selected_date)
        received_product_info_summary = getReceivedProductsSummary(received_product_info, selected_date)
        received_money_info = MoneyReceivedInformation.objects.filter(date__iexact = selected_date)
        received_money_info_summary = getTotalReceivedMoney(received_money_info)
        paid_money_info = MoneyPaidInformation.objects.filter(date__iexact = selected_date)
        paid_money_info_summary = getTotalPaidMoney(paid_money_info)
        miscellaneous_expenditure_info = MiscellaneousExpenditureInformation.objects.filter(date__iexact = selected_date)
        miscellaneous_expenditure_info_summary = getTotalExpenditure(miscellaneous_expenditure_info)
        net_amount = received_money_info_summary - paid_money_info_summary - miscellaneous_expenditure_info_summary
        profit = getProfit(supply_product_info)
        if len(selected_date)>0:
            date_label = "On "+selected_date
        else :
            date_label = selected_date
        supplyProductsFlag = True
        receiveProductsFlag = True
        receivedMoneyFlag = True
        paidMoneyFlag = True
        miscellaneousExpenditureFlag = True
        supplyProductsLabel = ""
        receiveProductsLabel = ""
        receivedMoneyLabel = ""
        paidMoneyLabel = ""
        miscellaneousExpenditureLabel = ""
        if len(list(supply_product_info)) <= 0:
            supplyProductsFlag = False
            supplyProductsLabel = "No Products Supplied On This Day"
        if len(list(received_product_info)) <= 0:
            receiveProductsFlag = False
            receiveProductsLabel = "No Products Received On This Day"
        if len(list(received_money_info)) <= 0:
            receivedMoneyFlag = False
            receivedMoneyLabel = "No Money Received On This Day"
        if len(list(paid_money_info)) <= 0:
            paidMoneyFlag = False
            paidMoneyLabel = "No Money Paid On This Day"
        if len(list(miscellaneous_expenditure_info)) <= 0:
            miscellaneousExpenditureFlag = False
            miscellaneousExpenditureLabel = "No Miscellaneous Expenditure On This Day"
        context = {
            "date_label": date_label,
            "supply_product_info":supply_product_info,
            "received_product_info":received_product_info,
            "received_money_info":received_money_info,
            "paid_money_info":paid_money_info,
            "miscellaneous_expenditure_info":miscellaneous_expenditure_info,
            "supplyProductsFlag":supplyProductsFlag,
            "supplyProductsLabel":supplyProductsLabel,
            "receiveProductsFlag":receiveProductsFlag,
            "receiveProductsLabel":receiveProductsLabel,
            "receivedMoneyFlag":receivedMoneyFlag,
            "receivedMoneyLabel":receivedMoneyLabel,
            "paidMoneyFlag":paidMoneyFlag,
            "paidMoneyLabel":paidMoneyLabel,
            "miscellaneousExpenditureFlag":miscellaneousExpenditureFlag,
            "miscellaneousExpenditureLabel":miscellaneousExpenditureLabel,
            "supply_product_info_summary":supply_product_info_summary,
            "received_product_info_summary":received_product_info_summary,
            "received_money_info_summary":received_money_info_summary,
            "paid_money_info_summary":paid_money_info_summary,
            "miscellaneous_expenditure_info_summary":miscellaneous_expenditure_info_summary,
            "net_amount":net_amount,
            "profit":profit

        }
        return render(request,"dayWiseSummaryView.html",context)
    return render(request,"dayWiseSummary.html",context)

def overallSummary(request):
    supply_product_info = SupplyProductsInformation.objects.filter()
    supply_product_info_summary = getSupplyProductsSummaryOverall(supply_product_info)
    received_product_info = Product.objects.filter()
    received_product_info_summary = getReceivedProductsSummaryOverall(received_product_info)
    received_money_info = MoneyReceivedInformation.objects.filter()
    received_money_info_summary = getTotalReceivedMoney(received_money_info)
    paid_money_info = MoneyPaidInformation.objects.filter()
    paid_money_info_summary = getTotalPaidMoney(paid_money_info)
    miscellaneous_expenditure_info = MiscellaneousExpenditureInformation.objects.filter()
    miscellaneous_expenditure_info_summary = getTotalExpenditure(miscellaneous_expenditure_info)
    net_amount = received_money_info_summary - paid_money_info_summary - miscellaneous_expenditure_info_summary
    profit = getProfit(supply_product_info)
    totalMoneyYetToPay = totalMoneyYetToPayOverall(received_product_info, paid_money_info)
    totalMoneyYetToReceive = totalMoneyYetToReceiveOverall(supply_product_info,received_money_info)
    date_label = "Overall Summary"
    supplyProductsFlag = True
    receiveProductsFlag = True
    supplyProductsLabel = ""
    receiveProductsLabel = ""
    if len(list(supply_product_info)) <= 0:
        supplyProductsFlag = False
        supplyProductsLabel = "No Products Supplied Yet"
    if len(list(received_product_info)) <= 0:
        receiveProductsFlag = False
        receiveProductsLabel = "No Products Received Yet"
    context = {
        "date_label": date_label,
        "supplyProductsFlag":supplyProductsFlag,
        "supplyProductsLabel":supplyProductsLabel,
        "receiveProductsFlag":receiveProductsFlag,
        "receiveProductsLabel":receiveProductsLabel,
        "supply_product_info_summary":supply_product_info_summary,
        "received_product_info_summary":received_product_info_summary,
        "received_money_info_summary":received_money_info_summary,
        "paid_money_info_summary":paid_money_info_summary,
        "miscellaneous_expenditure_info_summary":miscellaneous_expenditure_info_summary,
        "net_amount":net_amount,
        "profit":profit,
        "totalMoneyYetToPay":totalMoneyYetToPay,
        "totalMoneyYetToReceive":totalMoneyYetToReceive
    }

    return render(request,"overallSummary.html",context)

def monthWiseSummary(request):
    context = {

    }
    fromDate = request.POST.get("FromDate")
    toDate = request.POST.get("ToDate")
    if request.method == 'POST':
        supply_product_info = SupplyProductsInformation.objects.filter(date__range = [fromDate, toDate])
        supply_product_info_summary = getSupplyProductsSummaryMonthWise(supply_product_info, fromDate, toDate)
        received_product_info = Product.objects.filter(loading_date__range=[fromDate, toDate])
        received_product_info_summary = getReceivedProductsSummaryMonthWise(received_product_info, fromDate, toDate)
        received_money_info = MoneyReceivedInformation.objects.filter(date__range = [fromDate, toDate])
        received_money_info_summary = getTotalReceivedMoney(received_money_info)
        paid_money_info = MoneyPaidInformation.objects.filter(date__range = [fromDate, toDate])
        paid_money_info_summary = getTotalPaidMoney(paid_money_info)
        miscellaneous_expenditure_info = MiscellaneousExpenditureInformation.objects.filter(date__range = [fromDate, toDate])
        miscellaneous_expenditure_info_summary = getTotalExpenditure(miscellaneous_expenditure_info)
        net_amount = received_money_info_summary - paid_money_info_summary - miscellaneous_expenditure_info_summary
        profit = getProfit(supply_product_info)
        if len(fromDate) > 0 or len(toDate) > 0:
            date_label = " From "+fromDate + " To "+ toDate
        else :
            date_label = ""
        supplyProductsFlag = True
        receiveProductsFlag = True
        supplyProductsLabel = ""
        receiveProductsLabel = ""
        if len(list(supply_product_info)) <= 0:
            supplyProductsFlag = False
            supplyProductsLabel = "No Products Supplied In This Duration"
        if len(list(received_product_info)) <= 0:
            receiveProductsFlag = False
            receiveProductsLabel = "No Products Received In This Duration"
        context = {
            "date_label": date_label,
            "supplyProductsFlag":supplyProductsFlag,
            "supplyProductsLabel":supplyProductsLabel,
            "receiveProductsFlag":receiveProductsFlag,
            "receiveProductsLabel":receiveProductsLabel,
            "supply_product_info_summary":supply_product_info_summary,
            "received_product_info_summary":received_product_info_summary,
            "received_money_info_summary":received_money_info_summary,
            "paid_money_info_summary":paid_money_info_summary,
            "miscellaneous_expenditure_info_summary":miscellaneous_expenditure_info_summary,
            "net_amount":net_amount,
            "profit":profit
        }
        return render(request,"monthWiseSummaryView.html",context)
    return render(request,"monthWiseSummary.html",context)


def payDetailsConfirmation(request):
    return render(request,"payDetailsConfirmation.html",{})

def sendMoneyConfirmation(request):
    return render(request,"sendMoneyConfirmation.html",{})

def miscellaneousExpenditureConfirmation(request):
    return render(request,"miscellaneousExpenditureConfirmation.html",{})

def payDetailsError(request):
    return render(request,"payDetailsError.html",{})

def sendMoneyError(request):
    return render(request,"sendMoneyError.html",{})

def supplierTransactionsError(request):
    return render(request,"supplierTransactionsError.html",{})

def customerTransactionsError(request):
    return render(request,"customerTransactionsError.html",{})

def listOfUniqueLists(listOfLists):
    return map(list,set(map(tuple,listOfLists)))

def sumOfAvailableUnits(productList):
    total = 0
    for product in productList:
        total = total + product.quantity
    return total
def getBalanceAmountOfSupplier(supplier_name,city_name):
    receivedProductDetails = Product.objects.filter(Q(supplier__iexact=supplier_name)&Q(supplier_city__iexact = city_name))
    amountPaidDetails = MoneyPaidInformation.objects.filter(Q(supplier_name__iexact =supplier_name)&Q(city__iexact = city_name))

    total = 0
    for receivedProduct in list(receivedProductDetails):
        total = total + (receivedProduct.buying_price * receivedProduct.quantity )
    for amountPaidDetail in amountPaidDetails:
        total = total - amountPaidDetail.amount_paid
    return total

def getBalanceAmountOfCustomer(customer_name,city_name):
    suppliedProductDetails = SupplyProductsInformation.objects.filter(Q(customer_name__iexact=customer_name)&Q(city__iexact = city_name))
    amountReceivedDetails = MoneyReceivedInformation.objects.filter(Q(customer_name__iexact =customer_name)&Q(city__iexact = city_name))

    total = 0
    for suppliedProduct in list(suppliedProductDetails):
        total = total + (suppliedProduct.selling_price * suppliedProduct.quantity )
    for amountReceivedDetail in amountReceivedDetails:
        total = total - amountReceivedDetail.amount_paid
    return total

def getSupplyProductsSummary(supply_product_infos, date)  :
    supply_product_summary = []
    for supply_product_info in list(supply_product_infos):
        supply_product = []
        supply_product.append(supply_product_info.product_name)
        supply_product.append(supply_product_info.brand)
        supply_product.append(supply_product_info.weight)
        supply_product_summary.append(supply_product)
    supply_product_summary_unique = listOfUniqueLists(supply_product_summary)
    supply_product_summary_final = []
    for supplyProduct in supply_product_summary_unique:
        supply_product_details_final = {}
        supply_product_details_final["product_name"] = supplyProduct[0]
        supply_product_details_final["brand"] = supplyProduct[1]
        supply_product_details_final["weight"] = supplyProduct[2]
        supply_product_infos_final = SupplyProductsInformation.objects.filter(Q(product_name__iexact=supplyProduct[0])&Q(brand__iexact=supplyProduct[1])&Q(weight__iexact=supplyProduct[2])&Q(date__iexact=date))
        supply_product_details_final["total"] = sumOfAvailableUnits(supply_product_infos_final)
        supply_product_summary_final.append(supply_product_details_final)
    return supply_product_summary_final

def getSupplyProductsSummaryMonthWise(supply_product_infos, fromDate,toDate):
    supply_product_summary = []
    for supply_product_info in list(supply_product_infos):
        supply_product = []
        supply_product.append(supply_product_info.product_name)
        supply_product.append(supply_product_info.brand)
        supply_product.append(supply_product_info.weight)
        supply_product_summary.append(supply_product)
    supply_product_summary_unique = listOfUniqueLists(supply_product_summary)
    supply_product_summary_final = []
    for supplyProduct in supply_product_summary_unique:
        supply_product_details_final = {}
        supply_product_details_final["product_name"] = supplyProduct[0]
        supply_product_details_final["brand"] = supplyProduct[1]
        supply_product_details_final["weight"] = supplyProduct[2]
        supply_product_infos_final = SupplyProductsInformation.objects.filter(Q(product_name__iexact=supplyProduct[0])&Q(brand__iexact=supplyProduct[1])&Q(weight__iexact=supplyProduct[2])&Q(date__range=[fromDate,toDate]))
        supply_product_details_final["total"] = sumOfAvailableUnits(supply_product_infos_final)
        supply_product_summary_final.append(supply_product_details_final)
    return supply_product_summary_final

def getSupplyProductsSummaryOverall(supply_product_infos):
    supply_product_summary = []
    for supply_product_info in list(supply_product_infos):
        supply_product = []
        supply_product.append(supply_product_info.product_name)
        supply_product.append(supply_product_info.brand)
        supply_product.append(supply_product_info.weight)
        supply_product_summary.append(supply_product)
    supply_product_summary_unique = listOfUniqueLists(supply_product_summary)
    supply_product_summary_final = []
    for supplyProduct in supply_product_summary_unique:
        supply_product_details_final = {}
        supply_product_details_final["product_name"] = supplyProduct[0]
        supply_product_details_final["brand"] = supplyProduct[1]
        supply_product_details_final["weight"] = supplyProduct[2]
        supply_product_infos_final = SupplyProductsInformation.objects.filter(Q(product_name__iexact=supplyProduct[0])&Q(brand__iexact=supplyProduct[1])&Q(weight__iexact=supplyProduct[2]))
        supply_product_details_final["total"] = sumOfAvailableUnits(supply_product_infos_final)
        supply_product_summary_final.append(supply_product_details_final)
    return supply_product_summary_final


def getReceivedProductsSummary(received_product_infos, selected_date):
    received_product_summary = []
    for received_product_info in list(received_product_infos):
        received_product = []
        received_product.append(received_product_info.product_name)
        received_product.append(received_product_info.brand)
        received_product.append(received_product_info.weight)
        received_product_summary.append(received_product)

    received_product_summary_unique = listOfUniqueLists(received_product_summary)
    received_product_summary_final = []

    for receivedProduct in received_product_summary_unique:
        received_product_details_final = {}
        received_product_details_final["product_name"] = receivedProduct[0]
        received_product_details_final["brand"] = receivedProduct[1]
        received_product_details_final["weight"] = receivedProduct[2]
        received_product_infos_final = Product.objects.filter(Q(product_name__iexact=receivedProduct[0])&Q(brand__iexact=receivedProduct[1])&Q(weight__iexact=receivedProduct[2])&Q(loading_date__iexact=selected_date))
        received_product_details_final["total"] = sumOfAvailableUnits(received_product_infos_final)
        received_product_summary_final.append(received_product_details_final)
    return received_product_summary_final

def getReceivedProductsSummaryMonthWise(received_product_infos, fromDate, toDate):
    received_product_summary = []
    for received_product_info in list(received_product_infos):
        received_product = []
        received_product.append(received_product_info.product_name)
        received_product.append(received_product_info.brand)
        received_product.append(received_product_info.weight)
        received_product_summary.append(received_product)

    received_product_summary_unique = listOfUniqueLists(received_product_summary)
    received_product_summary_final = []

    for receivedProduct in received_product_summary_unique:
        received_product_details_final = {}
        received_product_details_final["product_name"] = receivedProduct[0]
        received_product_details_final["brand"] = receivedProduct[1]
        received_product_details_final["weight"] = receivedProduct[2]
        received_product_infos_final = Product.objects.filter(Q(product_name__iexact=receivedProduct[0])&Q(brand__iexact=receivedProduct[1])&Q(weight__iexact=receivedProduct[2])&Q(loading_date__range=[fromDate, toDate]))
        received_product_details_final["total"] = sumOfAvailableUnits(received_product_infos_final)
        received_product_summary_final.append(received_product_details_final)
    return received_product_summary_final

def getReceivedProductsSummaryOverall(received_product_infos):
    received_product_summary = []
    for received_product_info in list(received_product_infos):
        received_product = []
        received_product.append(received_product_info.product_name)
        received_product.append(received_product_info.brand)
        received_product.append(received_product_info.weight)
        received_product_summary.append(received_product)

    received_product_summary_unique = listOfUniqueLists(received_product_summary)
    received_product_summary_final = []

    for receivedProduct in received_product_summary_unique:
        received_product_details_final = {}
        received_product_details_final["product_name"] = receivedProduct[0]
        received_product_details_final["brand"] = receivedProduct[1]
        received_product_details_final["weight"] = receivedProduct[2]
        received_product_infos_final = Product.objects.filter(Q(product_name__iexact=receivedProduct[0])&Q(brand__iexact=receivedProduct[1])&Q(weight__iexact=receivedProduct[2]))
        received_product_details_final["total"] = sumOfAvailableUnits(received_product_infos_final)
        received_product_summary_final.append(received_product_details_final)
    return received_product_summary_final

def getTotalReceivedMoney(received_money_info):
    total = 0
    for received_money in received_money_info:
        total = total + received_money.amount_paid
    return total

def getTotalPaidMoney(paid_money_info):
    total = 0
    for paid_money in paid_money_info:
        total = total + paid_money.amount_paid
    return total
def getTotalExpenditure(miscellaneous_expenditure_info):
    total = 0
    for expenditure in miscellaneous_expenditure_info:
        total = total + expenditure.expenditure_amount
    return total

def getProfit(supply_product_info):
    profit = 0
    for supplyProduct in supply_product_info:
        sellingPrice = (supplyProduct.selling_price)*(supplyProduct.quantity)
        products = Product.objects.filter(Q(product_name__iexact=supplyProduct.product_name)&Q(brand__iexact=supplyProduct.brand)&Q(weight__iexact=supplyProduct.weight))
        buyingPrice = (list(products)[0].buying_price)*(supplyProduct.quantity)
        transportPrice = (list(products)[0].transport_price)*(supplyProduct.quantity)
        profit = profit + sellingPrice - buyingPrice - transportPrice

    return profit
def totalMoneyYetToPayOverall(received_product_info, paid_money_info):
    total = 0
    for product in list(received_product_info):
        total = total + ((product.buying_price+product.transport_price)*product.quantity)
    for paidMoney in paid_money_info:
        total = total - paidMoney.amount_paid
    return total
def totalMoneyYetToReceiveOverall(supply_product_info,received_money_info):
    total = 0
    for product in supply_product_info:
        total = total + (product.selling_price*product.quantity)
    for receivedMoney in received_money_info:
        total = total - receivedMoney.amount_paid
    return total