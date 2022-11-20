from django.shortcuts import render, redirect
from app.views import is_customer
import sweetify
from users.models import GreenBillUser
from merchant_software_apis.models import CustomerBill
from parking_lot_apis.models import SaveParkingLotBill
from petrol_pump_apis.models import SavePetrolPumpBill
from users.models import MerchantProfile
from category_and_tags.models import bill_category, bill_tags
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime
import string
import random
from merchant_software_apis.models import *
from promotions.models import *

from promotions.models import *
from bill_design.models import *
# Create your views here.


def Search_By_Customer(request):
    if request.method == "POST":
        if request.POST.get('TransferBtn') == 'Save':
            send_bill_id = request.POST['send_bill_id']
            send_bill_to_merchant = request.POST['send_bill_to_merchant']
            send_bill_data_table = request.POST['send_bill_data_table']
#
            # print(send_bill_id,'-----------------',send_bill_to_merchant,'-----------------',send_bill_data_table)

            if send_bill_to_merchant:
                merchant_business_id = MerchantProfile.objects.get(id = send_bill_to_merchant)
                user_id = GreenBillUser.objects.get(mobile_no = merchant_business_id.m_user)
            
            if request.POST['send_bill_data_table'] == "CustomerBill":


                customer_bill = CustomerBill.objects.filter(id =send_bill_id)

                letters = string.ascii_letters
                digit = string.digits
                random_string = str(customer_bill[0].id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

                customer_bill1 = MerchantBill.objects.create(user_id = customer_bill[0].user_id, mobile_no = customer_bill[0].mobile_no, email = customer_bill[0].email,
                        bill = customer_bill[0].bill, business_name = customer_bill[0].business_name, bill_received_business_name = merchant_business_id.id,
                        invoice_no = customer_bill[0].invoice_no, green_bill_transaction = customer_bill[0].green_bill_transaction, green_bill_print_transaction = customer_bill[0].green_bill_print_transaction,
                        print_transaction = customer_bill[0].print_transaction, bill_amount = customer_bill[0].bill_amount, customer_bill_category = customer_bill[0].customer_bill_category,stamp_id=customer_bill[0].stamp_id, exe_bill_type = customer_bill[0].exe_bill_type
                    )
                customer_bill_new = MerchantBill.objects.filter(id=customer_bill1.id).update(bill_url = random_string) 

                CustomerBill.objects.filter(id =customer_bill[0].id).update(delete_bill = True)
                sweetify.success(request, title="success", icon='success', text='Bill Transfer successfully !!!', timer=1500)

            elif request.POST['send_bill_data_table'] == "SaveParkingLotBill":

                parking_bill = SaveParkingLotBill.objects.filter(id=send_bill_id)

                try:
                    business_name1 = MerchantProfile.objects.get(id = parking_bill[0].m_business_id)
                except:
                    business_name1 = ""

                try:
                    bill_category_temp = bill_category.objects.get(id = parking_bill[0].bill_category_id)
                except:
                    bill_category_temp = ""

                customer_bill1 = MerchantBill.objects.create(user_id = parking_bill[0].user_id, mobile_no = parking_bill[0].mobile_no,
                        bill = parking_bill[0].bill_file, business_name = business_name1, bill_received_business_name = merchant_business_id.id,
                        invoice_no = parking_bill[0].invoice_no, 
                        bill_amount = parking_bill[0].total, customer_bill_category = bill_category_temp
                    )

                letters = string.ascii_letters
                digit = string.digits
                random_string = str(parking_bill[0].id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

                customer_bill_new = MerchantBill.objects.filter(id=customer_bill1.id).update(bill_url = random_string) 

                SaveParkingLotBill.objects.filter(id=parking_bill[0].id).update(delete_bill = True)

                sweetify.success(request, title="success", icon='success', text='Bill Transfer successfully !!!', timer=1500)

            elif request.POST['send_bill_data_table'] == "SavePetrolPumpBill":

                petrol_pump = SavePetrolPumpBill.objects.filter(id=send_bill_id)

                business_name1 = MerchantProfile.objects.get(id = petrol_pump[0].m_business_id)
                

                try:
                    bill_category_temp = bill_category.objects.get(id = petrol_pump[0].bill_category_id)
                except:
                    bill_category_temp = ""

                customer_bill1 = MerchantBill.objects.create(user_id = petrol_pump[0].user_id, mobile_no = petrol_pump[0].mobile_no,
                    bill = petrol_pump[0].bill_file, business_name = business_name1, bill_received_business_name = merchant_business_id.id,
                    invoice_no = petrol_pump[0].invoice_no, 
                    bill_amount = petrol_pump[0].total_amount, customer_bill_category = bill_category_temp
                )

                letters = string.ascii_letters
                digit = string.digits
                random_string = str(petrol_pump[0].id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

                customer_bill_new = MerchantBill.objects.filter(id=customer_bill1.id).update(bill_url = random_string)

                SavePetrolPumpBill.objects.filter(id=petrol_pump[0].id).update(delete_bill = True)

                sweetify.success(request, title="success", icon='success', text='Bill Transfer successfully !!!', timer=1500)
            else:
                sweetify.error(request, title="error", icon='error', text='Failed to Transfer!!!', timer=1500)

        if request.POST.get('submitBtn') == 'Update':
            bill_id = request.POST['bill_id']
            updated_bill_tags = ''
            db_table = request.POST['edit_db_table']
            tags_list = []
            bill_tags_value = request.POST['edit_bill_tags_value']
            edit_amount_exe = request.POST['edit_amount']
            edit_category_exe =  request.POST['edit_category']
            edit_remarks = request.POST.get('edit_remarks',None)
            tags_list = bill_tags_value.split(",")
            

            # print("edit_amount_exe",edit_amount_exe)

            if bill_tags_value:
                updated_tags_list = []
                for tag in tags_list:
                    if tag.isdigit():
                        updated_tags_list.append(tag)
                    else:
                        result = bill_tags.objects.create(bill_tags_name=tag,user_id=GreenBillUser.objects.get(id=request.user.id),is_customer_bill_tag=1)
                        tag = result.id
                        updated_tags_list.append(tag)

                updated_bill_tags = ','.join(map(str, updated_tags_list))
            

            # print('--------------------------',edit_remarks,'---------------',db_table)

            if db_table == "CustomerBill":
                # print('11',bill_id)
                try:
                    CustomerBill.objects.filter(id=bill_id).update(business_name=request.POST.get('edit_business'), customer_bill_category = edit_category_exe, bill_amount = edit_amount_exe, bill_tags = updated_bill_tags, remarks = request.POST.get("edit_remarks"), custom_business_name = request.POST.get("edit_custom_business"))


                    # if request.FILES['editfile']:
                    #     CustomerBill.objects.filter(id=bill_id).update(business_name=request.POST.get('edit_business'), customer_bill_category=request.POST.get('edit_category'), bill_amount=request.POST.get('edit_amount'), bill_date=request.POST['edit_date'], bill_tags = updated_bill_tags, remarks = request.POST.get("edit_remarks"), custom_business_name = request.POST.get("edit_custom_business"), invoice_no = request.POST.get("edit_invoice_no"))
                    #     bill_data = CustomerBill.objects.get(id=bill_id)
                    #     bill_data.bill = request.FILES['editfile']
                    #     bill_data.save()
                    #     print('bill_data',bill_data)
                    # else:
                    #     CustomerBill.objects.filter(id=bill_id).update(business_name=request.POST.get('edit_business'), customer_bill_category=request.POST.get('edit_category'), bill_amount=request.POST.get('edit_amount'), bill_date=request.POST['edit_date'], bill_tags = updated_bill_tags, remarks = request.POST.get("edit_remarks"), custom_business_name = request.POST.get("edit_custom_business"), invoice_no = request.POST.get("edit_invoice_no"))
                    #     print('tryelse')
                except:

                    CustomerBill.objects.filter(id=bill_id).update(business_name=request.POST.get('edit_business'), customer_bill_category=request.POST.get('edit_category'), bill_amount=request.POST.get('edit_amount'), bill_tags = updated_bill_tags, remarks = request.POST.get("edit_remarks"), custom_business_name = request.POST.get("edit_custom_business"))
                    # print('tryexcept')

            elif db_table == "SaveParkingLotBill":
                # print('parking')
                SaveParkingLotBill.objects.filter(id=bill_id).update(bill_category_id=request.POST.get('edit_category'), bill_tags = updated_bill_tags, remarks = request.POST.get("edit_remarks"))

            elif db_table == "SavePetrolPumpBill":
               # print("petrol")
               SavePetrolPumpBill.objects.filter(id=bill_id).update(bill_category_id=request.POST.get('edit_category'), bill_tags = updated_bill_tags, remarks = request.POST.get("edit_remarks"))

            sweetify.success(request, title="Success", icon='success', text='Bill Updated Successfully', timer=1500)

        base_url = "http://157.230.228.250/"
        updated_search_list=[]
        search_list = []
        bill_category_temp1 = ''
        business_name1 = ''
        keyword = request.POST['search_keyword']
        customer_bill_list = CustomerBill.objects.filter(Q(customer_bill_category__bill_category_name__icontains=keyword)|Q(business_name__m_business_name__icontains=keyword)|Q(customer_bill_category__bill_category_name__exact=keyword)|Q(business_name__m_business_name__exact=keyword),mobile_no = request.user.mobile_no, delete_bill = False)

        for bill in customer_bill_list:

            if bill.bill_tags:
                bill_tags_temp = bill.bill_tags
            else:
                bill_tags_temp = "0"

            try:
                bill_file = bill.bill
            except:
                bill_file = ""

            # base url + work have to done
            if bill.customer_added == True:
                new_bill_url = str(base_url) + 'self-added-bill/' + str(bill.bill_url) + "/"
            else:
                new_bill_url = str(base_url) + 'my-bill/' + str(bill.bill_url) + "/"


            updated_search_list.append({
                'id':bill.id,
                'amount': str(bill.bill_amount),
                'bill_url': new_bill_url,
                'invoice_no': bill.invoice_no,
                'amount': str(bill.bill_amount),
                'bill_date': bill.bill_date,
                'bill_category' : bill.customer_bill_category,
                'business_name' : bill.business_name,
                'bill_tags' : bill_tags_temp,
                'remarks' : bill.remarks,
                'bill_file':bill_file,
                'db_table': "CustomerBill",
                'customer_added':bill.customer_added,
                'custom_business_name': bill.custom_business_name,
            })

        parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no=request.user.mobile_no, delete_bill = False) 
        for bill in parking_bill_list:
            if bill.bill_tags:
                bill_tags_temp = bill.bill_tags
            else:
                bill_tags_temp = "0"

            try:
                business_name = MerchantProfile.objects.get(id = bill.m_business_id)
                business_name1 = business_name.m_business_name
            except:
                business_name = ""

            try:
                bill_file = bill.bill_file
            except:
                bill_file = ""

            try:
                bill_category_temp = bill_category.objects.get(id = bill.bill_category_id)
                bill_category_temp1=bill_category_temp.bill_category_name
            except:
                bill_category_temp = ""
            
            if bill_category_temp1.lower() == keyword.lower() or business_name1.lower() == keyword.lower():
                updated_search_list.append({
                        'id':bill.id,
                        'amount': str(bill.amount),
                        'bill_url':str(base_url) + 'parking-lot-bill/' + str(bill.bill_url) + "/",
                        'invoice_no': bill.invoice_no,
                        'amount': str(bill.amount),
                        'bill_date': datetime.strptime(bill.date, "%d-%m-%Y").date(),
                        'bill_category' : bill_category_temp,
                        'business_name' : business_name,
                        'bill_tags' : bill_tags_temp,
                        'remarks' : bill.remarks,
                        'custom_business_name': "",
                        'db_table': "SaveParkingLotBill",
                        'customer_added': False,
                        'bill_file':bill_file,
                })

        
        petrol_pump_bill_list = SavePetrolPumpBill.objects.filter(mobile_no=request.user.mobile_no, delete_bill = False)
        for bill in petrol_pump_bill_list:
            if bill.bill_tags:
                bill_tags_temp = bill.bill_tags
            else:
                bill_tags_temp = "0"

            try:
                bill_file = bill.bill_file
            except:
                bill_file = ""

            if bill.bill_tags:
                bill_tags_temp = bill.bill_tags
            else:
                bill_tags_temp = "0"

            try:
                business_name = MerchantProfile.objects.get(id = bill.m_business_id)
                business_name1 = business_name.m_business_name
            except:
                business_name = ""

            try:
                bill_category_temp = bill_category.objects.get(id = bill.bill_category_id)
                bill_category_temp1 = bill_category_temp.bill_category_name
            except:
                bill_category_temp = ""

            if bill_category_temp1.lower() == keyword.lower() or business_name1.lower() == keyword.lower():
                updated_search_list.append({
                    'id':bill.id,
                    'amount': str(bill.total_amount),
                    'bill_url': str(base_url) + 'petrol-pump-bill/' + str(bill.bill_url) + "/",
                    'invoice_no': bill.invoice_no,
                    'amount': str(bill.total_amount),
                    'bill_date': datetime.strptime(bill.date, "%d-%m-%Y").date(),
                    'bill_category' : bill_category_temp,
                    'business_name' : business_name,
                    'bill_tags' : bill_tags_temp,
                    'remarks' : bill.remarks,
                    'custom_business_name': "",
                    'db_table': "SavePetrolPumpBill",
                    'bill_file':bill_file,
                    'customer_added': False,
                })




        # bill_category_name = bill_category.objects.all()
        # b_name = MerchantProfile.objects.all()

        # customer_bill_tags = bill_tags.objects.all() 

        # all_cust_bill = search_list

        # for cust_bill in all_cust_bill:

        #     bill_tags1 = cust_bill.bill_tags

        #     if cust_bill.bill_tags:
        #         bill_tags_list = list(bill_tags1.split(","))

        #     else:
        #         bill_tags_list = ""

        #     bill_tags2 = []
        
        #     if bill_tags1:

        #         for x in range(len(bill_tags_list)):

        #             try:

        #                 bill_tags1 = bill_tags.objects.get(id=bill_tags_list[x])

        #                 bill_tags2.append(bill_tags1.bill_tags_name)

        #             except:

        #                 print("")

        #     bill_tags3 = ', '.join(map(str, bill_tags2))

        #     cust_bill.bill_tags_name = bill_tags3

        # search_list.append(bills_categories)
        # print('search_list',search_list)
        bill_category_name = bill_category.objects.all()
        b_name = MerchantProfile.objects.all()
        customer_bill_tags = bill_tags.objects.all()
        customer_merchant_businesses = MerchantProfile.objects.filter(m_user = request.user)

        context = {
            'search_list': updated_search_list,
            'bill_category' : bill_category_name,
            'business_names' : b_name,
            'bill_tags': customer_bill_tags,
            'search_keyword':keyword,
            'customer_merchant_businesses':customer_merchant_businesses,
        }
        return render(request, "customer/customer_search/search_list.html", context)
    else:
        context = {}
        return render(request, "customer/customer_search/search_list.html", context)





# def Search_By_Customer(request):
#     if request.method == "POST":
#         updated_search_list=[]
#         search_list = []
#         keyword = request.POST['search_keyword']
#         customer_bill_list = CustomerBill.objects.filter(Q(customer_bill_category__bill_category_name__icontains=keyword)|Q(business_name__m_business_name__icontains=keyword)|Q(customer_bill_category__bill_category_name__exact=keyword)|Q(business_name__m_business_name__exact=keyword),mobile_no = request.user.mobile_no)

#         for bill in customer_bill_list:

#             if bill.bill_tags:
#                 bill_tags_temp = bill.bill_tags
#             else:
#                 bill_tags_temp = "0"

#             updated_search_list.append({
#                 'id': bill.id,
#                 'amount': str(bill.bill_amount),
#                 'bill_date': bill.bill_date,
#                 'bill_category' : bill.customer_bill_category,
#                 'business_name' : bill.business_name,
#                 'bill_tags' : bill_tags_temp,
#                 'remarks' : bill.remarks,
#                 'custom_business_name': bill.custom_business_name,
#             })

#         parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no=request.user.mobile_no) 
#         for bill in parking_bill_list:
#             if bill.bill_tags:
#                 bill_tags_temp = bill.bill_tags
#             else:
#                 bill_tags_temp = "0"

#             try:
#                 business_name = MerchantProfile.objects.get(id = bill.m_business_id)
#             except:
#                 business_name = ""
#             try:
#                 bill_category_temp = bill_category.objects.get(id = bill.bill_category_id)
#             except:
#                 bill_category_temp = ""
            
#             if bill_category_temp == keyword:
#                 updated_search_list.append({
#                         'id': bill.id,
#                         'amount': str(bill.amount),
#                         'bill_date': datetime.strptime(bill.date, "%d-%m-%Y").date(),
#                         'bill_category' : bill_category_temp,
#                         'business_name' : business_name,
#                         'bill_tags' : bill_tags_temp,
#                         'remarks' : bill.remarks,
#                         'custom_business_name': ""
#                 })

        
#         petrol_pump_bill_list = SavePetrolPumpBill.objects.filter(mobile_no=request.user.mobile_no)
#         for bill in petrol_pump_bill_list:
#             if bill.bill_tags:
#                 bill_tags_temp = bill.bill_tags
#             else:
#                 bill_tags_temp = "0"
#             try:
#                 business_name = MerchantProfile.objects.get(id = bill.m_business_id)
#             except:
#                 business_name = ""
#             try:
#                 bill_category_temp = bill_category.objects.get(id = bill.bill_category_id)
#             except:
#                 bill_category_temp = ""

#             if bill_category_temp == keyword:
#                 updated_search_list.append({
#                     'id': bill.id,
#                     'amount': str(bill.total_amount),
#                     'bill_date': datetime.strptime(bill.date, "%d-%m-%Y").date(),
#                     'bill_category' : bill_category_temp,
#                     'business_name' : business_name,
#                     'bill_tags' : bill_tags_temp,
#                     'remarks' : bill.remarks,
#                     'custom_business_name': ""
#                 })




#         # bill_category_name = bill_category.objects.all()
#         # b_name = MerchantProfile.objects.all()

#         # customer_bill_tags = bill_tags.objects.all() 

#         # all_cust_bill = search_list

#         # for cust_bill in all_cust_bill:

#         #     bill_tags1 = cust_bill.bill_tags

#         #     if cust_bill.bill_tags:
#         #         bill_tags_list = list(bill_tags1.split(","))

#         #     else:
#         #         bill_tags_list = ""

#         #     bill_tags2 = []
        
#         #     if bill_tags1:

#         #         for x in range(len(bill_tags_list)):

#         #             try:

#         #                 bill_tags1 = bill_tags.objects.get(id=bill_tags_list[x])

#         #                 bill_tags2.append(bill_tags1.bill_tags_name)

#         #             except:

#         #                 print("")

#         #     bill_tags3 = ', '.join(map(str, bill_tags2))

#         #     cust_bill.bill_tags_name = bill_tags3

#         # search_list.append(bills_categories)
#         # print('search_list',search_list)
#         context = {
#             'search_list': updated_search_list,
#         }
#         return render(request, "customer/customer_search/search_list.html", context)
#     else:
#         context = {}
#         return render(request, "customer/customer_search/search_list.html", context)






