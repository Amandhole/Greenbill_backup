from django.urls import path
from .views import *

urlpatterns = [
    path("bill-feedback/", bill_feedback, name="bill-feedback"),
    path("update-bill-feedback-rating/<int:id>/", update_bill_feedback_rating, name="update-bill-feedback-rating"),
    path("customer_reply/",customer_reply, name="customer_reply"), 
    path("feedback_reply/",feedback_reply, name="feedback_reply"), 
    path("reply-by-id/", reply_by_id, name="reply-by-id"),
]
