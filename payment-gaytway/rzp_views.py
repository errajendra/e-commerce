import razorpay
import os
import requests
from django.shortcuts import HttpResponse, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from ecommerce_app.models import Order
from .serializers import CreatePaymentLinkSerialiser

RZP_KAY_ID = settings.RAZORPAY_KAY_ID
RZP_SECRETE_KEY = settings.RAZORPAY_SECRETE_KEY
APP_NAME = settings.RAZORPAY_APP_NAME

rzp_client = razorpay.Client(auth=(RZP_KAY_ID, RZP_SECRETE_KEY))


# Changes required
@csrf_exempt
def create_rzp_order_link(request):
    """
    creating RazorPay payment link
    """
    try:
        host = f"{request.scheme}://{request.META['HTTP_HOST']}"
        serializer = CreatePaymentLinkSerialiser(data=request.GET)
        if not serializer.is_valid():
            return HttpResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        data = serializer.data
        tnx_id = data['tnx_id']
        amount = int(data['amount']) * 100

        redirect_to = host + str('/payment/webhook-rzp/') + f"{tnx_id}/"
        # redirect_to = "https://coursetube.in/payment/create-phonerpay-order-link/"
        callback_url = redirect_to

        rzp_response = rzp_client.payment_link.create({
            "upi_link": True,
            "amount": amount,
            "currency": "INR",
            "accept_partial": False,
            # "first_min_partial_amount": 100,
            "description": "For Purchase purpose",
            "reference_id": str(tnx_id),
            "customer": {
                "name": data['customer_name'],
                # "email": data['customer_email'],
                "contact": data['customer_phone']
            },
            "notify": {
                "sms": True,
                "email": False
            },
            "reminder_enable": False,
            "notes": {
                "policy_name": "Deposite"
            },
            "callback_url": callback_url,
            "callback_method": "get"
        })
        
        if rzp_response:
            pay_url = rzp_response['short_url']
            return HttpResponse(f'<meta name="referrer" content="strict-origin-when-cross-origin"><script type="text/javascript">window.location.href="{pay_url}";</script>')

            # return_url = host + reverse('phonepay_webhook') + f'?ref={pay_url}'
            # return HttpResponseRedirect(pay_url)
            # return return_url
        
        return HttpResponse({"messsage": "Invaolid payload", "data": rzp_response}, status=500)
    
    except Exception as ex:
        print(ex)
        return HttpResponse(f"PG: {ex}")
    



@csrf_exempt
def verify_rzp_payment(request):
    razorpay_order_id = request.POST.get('razorpay_order_id')
    razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
    razorpay_signature = request.POST.get('razorpay_signature', '')

    # try:
    #     tran_id = int(tran_id)
    # except:
    #     if tran_id[0] == 'C':
    #         ord = get_object_or_404(Order, id=int(tran_id[1:]))
    #         ord.status = "DELIVERED"
    #         ord.save()
    #     return redirect("account")
    
    try:
        rzp_sign = rzp_client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })

        frontend_url = os.environ.get("FRONTEND_URL")
        redirect_front = frontend_url + '/recharge/'
        frontend_webhook = frontend_url + '/webhook/phonepay/'

        if rzp_sign:
            return redirect(reversed('payment_successful'))
        else:
            return redirect(reversed('payment_failed'))
    except:
        pass
    finally:
        return redirect(redirect_front)
