from django.shortcuts import render, redirect
from merchant_software_apis.models import CustomerBill
import sweetify
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse
import datetime
from app.views import is_customer

@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def customer_shopping_analysis_by_category(request):
    labels = []
    data = []

    queryset = CustomerBill.objects.filter(mobile_no=request.user.mobile_no)
  
    # date in yyyy/mm/dd format 
    # d1 = datetime.date(2020, 1, 3)
    # d2 = datetime.date(2021, 1, 30) 

    for bills in queryset:
        if bills.customer_bill_category:
            if bills.customer_bill_category.bill_category_name in labels:
                print("available")
            else:
                labels.append(bills.customer_bill_category.bill_category_name)

    spend_by_bill_category = {new_list: 0 for new_list in labels} 

    customer_bills = CustomerBill.objects.filter(mobile_no=request.user.mobile_no)

    for oject in customer_bills:
        for x in labels:
            if oject.customer_bill_category:
                if oject.customer_bill_category.bill_category_name == x:
                    spend_by_bill_category[x] =  spend_by_bill_category[x] + oject.bill_amount

    for object in spend_by_bill_category:
        data.append(spend_by_bill_category[object])

    context = {
            "ShoppingAnalysisNavclass": "active",
            "ShoppingAnalysisCollapseShow": "show",
            "ShoppingAnalysisCategoryNavclass": "active"
    }

    context['from_date'] = ""
    context['to_date'] = ""

    

    if request.method == 'POST':

        labels = []
        data = []

        from_date = datetime.datetime.strptime(request.POST["from_date"], "%Y-%m-%d").date()
        to_date = datetime.datetime.strptime(request.POST["to_date"], "%Y-%m-%d").date()

        for bills in queryset:
            if bills.bill_date >= from_date and bills.bill_date <= to_date:
                if bills.customer_bill_category:
                    if bills.customer_bill_category.bill_category_name in labels:
                        print("available")
                    else:
                        labels.append(bills.customer_bill_category.bill_category_name)

        spend_by_bill_category = {new_list: 0 for new_list in labels}

        customer_bills = CustomerBill.objects.filter(mobile_no=request.user.mobile_no)

        for oject in customer_bills:
            if oject.bill_date >= from_date and oject.bill_date <= to_date:
                for x in labels:
                    if oject.customer_bill_category:
                        if oject.customer_bill_category.bill_category_name == x:
                            spend_by_bill_category[x] =  spend_by_bill_category[x] + oject.bill_amount

        for object in spend_by_bill_category:
            data.append(spend_by_bill_category[object])

        context['from_date'] = request.POST["from_date"]
        context['to_date'] = request.POST["to_date"]

    context['data'] = data
    context['labels'] = labels

    return render(request, "customer/shopping_analysis/shopping-analysis-category.html", context)


@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def customer_shopping_analysis_by_merchant(request):
    labels = []
    data = []

    queryset = CustomerBill.objects.filter(mobile_no=request.user.mobile_no)
  
    # date in yyyy/mm/dd format 
    # d1 = datetime.date(2020, 1, 3)
    # d2 = datetime.date(2021, 1, 30) 

    for bills in queryset:
        if bills.business_name:
            if bills.business_name.m_business_name in labels:
                print("available")
            else:
                labels.append(bills.business_name.m_business_name)

    spend_by_bill_business = {new_list: 0 for new_list in labels} 

    customer_bills = CustomerBill.objects.filter(mobile_no=request.user.mobile_no)

    for oject in customer_bills:
        for x in labels:
            if oject.business_name:
                if oject.business_name.m_business_name == x:
                    spend_by_bill_business[x] =  spend_by_bill_business[x] + oject.bill_amount

    for object in spend_by_bill_business:
        data.append(spend_by_bill_business[object])

    context = {
            "ShoppingAnalysisNavclass": "active",
            "ShoppingAnalysisCollapseShow": "show",
            "ShoppingAnalysisMerchantNavclass": "active"
    }

    context['from_date'] = ""
    context['to_date'] = ""

    from_date = ""
    to_date = ""

    if request.method == 'POST':

        labels = []
        data = []

        from_date = datetime.datetime.strptime(request.POST["from_date"], "%Y-%m-%d").date()
        to_date = datetime.datetime.strptime(request.POST["to_date"], "%Y-%m-%d").date()
        
        for bills in queryset:
            if bills.bill_date >= from_date and bills.bill_date <= to_date:
                if bills.business_name:
                    if bills.business_name.m_business_name in labels:
                        print("available")
                    else:
                        labels.append(bills.business_name.m_business_name)

        spend_by_bill_business = {new_list: 0 for new_list in labels} 

        customer_bills = CustomerBill.objects.filter(mobile_no=request.user.mobile_no)

        # print(from_date)
        # print(to_date)

        for oject in customer_bills:
            if oject.bill_date >= from_date and oject.bill_date <= to_date:
                for x in labels:
                    if oject.business_name:
                        if oject.business_name.m_business_name == x:
                            spend_by_bill_business[x] =  spend_by_bill_business[x] + oject.bill_amount

        for object in spend_by_bill_business:
            data.append(spend_by_bill_business[object])

        context['from_date'] = request.POST["from_date"]
        context['to_date'] = request.POST["to_date"]

    context['data'] = data
    context['labels'] = labels

    return render(request, "customer/shopping_analysis/shopping-analysis-merchant.html", context)