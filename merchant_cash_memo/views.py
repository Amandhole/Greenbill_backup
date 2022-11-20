from django.shortcuts import render
from cash_memo_receipts.models import Cash_Memos
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_merchant_or_merchant_staff
# Create your views here.

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def view_all_cash_memo(request):
    context = {
                'merchantCashMemoNavClass':'active',
            }
    return render(request, "merchant/merchant_cash_memo/merchant_cash_memo.html",context)
