from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    
    path("get-number-of-visit/", views.Number_of_views_in_merchant, name="get-number-of-visit"),
    path("merchant-offers/",views.merchant_offers,name="merchant-offers"),
    path("merchant_offers_view/",views.merchant_offer_view,name="merchant_offers_view"),
    path("merchant-view-offer/",views.merchant_view_offer,name="merchant-view-offer"),
    path("delete-offer/<int:id>", views.Delete_Offer, name="delete-offer"),
    path("view-offer-details/<int:id>",views.view_offer_details, name="view-offer-details"),
    path("partner-offer/",views.partner_offer_view,name="partner-offer"),
    path("view-partner-offer-details/<int:id>",views.view_partner_offer_record, name="view-partner-offer-details"),

    path("get-state-by-business-ids/",views.get_state_by_business_ids, name="get-state-by-business-ids"),
    
    path("get-business-by-state-ids/",views.get_business_by_state_ids, name="get-business-by-state-ids"),
    
    path("get-business-by-state-ids-for-merchant/",views.get_business_by_state_ids_for_merchant, name="get-business-by-state-ids-for-merchant"),

    path("get-city-by-state-names/",views.get_city_by_state_names, name="get-city-by-state-names"),

    path("get-area-by-city-names/",views.get_area_by_city_names, name="get-area-by-city-names"),

    # path("get-views/",views.Number_of_views_in_merchant, name="get-views"),

    path("get-city-by-state-ids-in-offers/", views.get_city_by_state_ids_in_offers, name="get-city-by-state-ids-in-offers"),

    path("get-area-by-city-names-in-offers/", views.get_area_by_city_names_in_offers, name="get-area-by-city-names-in-offers"),

    path("get-customers-by-state/", views.get_customers_by_state, name="get-customers-by-state"),

    path("get-customers-by-city/", views.get_customers_by_city, name="get-customers-by-city"),
 
    path("get-customers-by-area/", views.get_customers_by_area, name="get-customers-by-area"),

    path("get-merchant-by-state/", views.get_all_merchants_by_state, name="get-merchant-by-state"),

    path("get-merchants-by-area/", views.get_merchants_by_area, name="get-merchants-by-area"),

    path("cost-by-state-per-customer/", views.get_customers_cost_by_state, name="cost-by-state-per-customer"),

    path("cost-by-state-per-merchant/", views.get_merchant_cost_by_state, name="cost-by-state-per-merchant"),

    path("total-cost-by-customer-in-offer/", views.get_customers_cost_by_area, name="total-cost-by-customer-in-offer"),

    path("total-cost-by-merchant-in-offer/", views.get_merchants_cost_by_area, name="total-cost-by-merchant-in-offer"),

    path("get-partner-city-by-state-names-in-offers/",views.GetPartnerCity, name="get-partner-city-by-state-names-in-offers"),

    path("get-partner-area-by-city-names-in-offers/",views.GetPartnerArea, name="get-partner-area-by-city-names-in-offers"),

    path("get-partners-count/", views.GetPartnersCountByState, name="get-partners-count"),

    path("get-partner-cost/", views.GetPartnerCost, name="get-partner-cost"),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
