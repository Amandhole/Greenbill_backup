from django.urls import path
from .views import *

urlpatterns = [

   path('bulk-email-customer/',BulkEmailCustomer,name="bulk-email-customer"),
   path('bulk-sms-customer/',BulkSmsCustomer,name='bulk-sms-customer'),
   path('delete-customer-bulk-mail/<int:id>', deletebulksmsemail,name="delete-customer-bulk-mail"),
   path('sms-header/',smsHeader, name="sms-header"),
   path('sms-template/',smsTemplate, name="sms-template"),

   path('download-sample-contact-file/',download_sample_contact_file,name="download-sample-contact-file"),
   path('download-sample-email-file/',download_sample_email_file,name="download-sample-email-file"),

   path("get-city-by-state-ids-in-merchant-bulk-sms/", get_city_by_state_ids_in_merchant_bulk_sms, name="get-city-by-state-ids-in-merchant-bulk-sms"),
   path("get-area-by-city-names-in-merchant-bulk-sms/", get_area_by_city_names_in_merchant_bulk_sms, name="get-area-by-city-names-in-merchant-bulk-sms"),

   path("get-city-by-state-ids-in-merchant-bulk-email/", get_city_by_state_ids_in_merchant_bulk_email, name="get-city-by-state-ids-in-merchant-bulk-email"),
   path("get-area-by-city-names-in-merchant-bulk-email/", get_area_by_city_names_in_merchant_bulk_email, name="get-area-by-city-names-in-merchant-bulk-email"),

   path('get-template-by-header/',get_template_by_header,name="get-template-by-header"),
   

   path('get-customer-count-by-state-city-area/',get_customer_count_by_state_city_area,name="get-customer-count-by-state-city-area"),


]
