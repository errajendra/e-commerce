import os
import json
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['post'])
def payu_success_webhook(request):
    data = request.POST
    response = requests.post(
        url = 'https://pronexatrad.in/webhook/payu-success/',
        data = data
    )
    with open("webhook_pay_success.txt", 'w') as file:
        if response.status_code == 200:
            file.write("")
        else:
            file.write(json.dumps(data))
    # call treding api according to payment status 

    return Response({"message": "OK"})


@api_view(['post'])
def payu_fail_webhook(request):
    data = request.POST
    response = requests.post(
        url = 'https://pronexatrad.in/webhook/payu-failed/',
        data = data
    )
    with open("webhook_pay_failed.txt", 'w') as file:
        if response.status_code == 200:
            file.write("")
        else:
            file.write(json.dumps(data))

    # call treding api according to payment status 

    return Response({"message": "Failed"})


@api_view(['post', 'get'])
def rzp_webhook(request):
    response = request.data
    pay_event = response['event']
    tnx_id = response['payload']['payment_link']['entity']['reference_id'] # Mch ref id
    order_id = response['payload']['payment_link']['entity']['order_id'] # rzp order_id
    frontend_url = os.environ.get("FRONTEND_URL")
    frontend_webhook = frontend_url + '/webhook/phonepay/'

    if pay_event == 'payment_link.paid':
        front_webhook_res = requests.post(
            url = frontend_webhook, 
            data={
                "tnxid": tnx_id,
                "success": True,
                "providerReferenceId": order_id
            }
        )

    elif pay_event == "payment_link.expired":
        front_webhook_res = requests.post(
            url = frontend_webhook, 
            data={
                "tnxid": tnx_id,
                "success": False,
                "providerReferenceId": order_id
            }
        )
    
    elif pay_event == "payment_link.cancelled":
        front_webhook_res = requests.post(
            url = frontend_webhook, 
            data={
                "tnxid": tnx_id,
                "success": False,
                "providerReferenceId": order_id
            }
        )
    
    return Response({"message": "OK"})