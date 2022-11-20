from django.shortcuts import render, redirect

import sweetify
from users.models import GreenBillUser
from merchant_software_apis.models import CustomerBill
from users.models import MerchantProfile
from category_and_tags.models import bill_category, bill_tags
# Create your views here.


def Search_By_Customer(request):
    if request.method == "POST":
        search_list = []
        keyword = request.POST['search_keyword']
        qs = CustomerBill.objects.all().filter(
            mobile_no=request.user.mobile_no, customer_bill_category__bill_category_name__icontains=keyword)

        qs2 = CustomerBill.objects.all().filter(
            business_name__m_business_name__icontains=keyword, mobile_no=request.user.mobile_no)

        for object in qs:
            search_list.append(object)
        for object in qs2:
            search_list.append(object)



    bill_category_name = bill_category.objects.all()
    b_name = MerchantProfile.objects.all()

    customer_bill_tags = bill_tags.objects.all() 

    all_cust_bill = search_list

    for cust_bill in all_cust_bill:

        bill_tags1 = cust_bill.bill_tags

        if cust_bill.bill_tags:
            bill_tags_list = list(bill_tags1.split(","))

        else:
            bill_tags_list = ""

        bill_tags2 = []
    
        if bill_tags1:

            for x in range(len(bill_tags_list)):

                try:

                    bill_tags1 = bill_tags.objects.get(id=bill_tags_list[x])

                    bill_tags2.append(bill_tags1.bill_tags_name)

                except:

                    print("")

        bill_tags3 = ', '.join(map(str, bill_tags2))

        cust_bill.bill_tags_name = bill_tags3
        context = {
            'search_list': search_list,
            "customer_bill": all_cust_bill,
        }
        return render(request, "customer/customer_search/search_list.html", context)
    else:
        context = {}
        return render(request, "customer/customer_search/search_list.html", context)


