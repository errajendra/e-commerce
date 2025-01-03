import os
import json
import base64
import hashlib
import requests
from django.conf import settings
from django.shortcuts import HttpResponse, render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .serializers import CreatePaymentLinkSerialiser


@csrf_exempt
def create_pg_order_link(request):
    """
    creating PhonePay payment link
    """
    # try:
    host = f"{request.scheme}://{request.META['HTTP_HOST']}"
    merchantId = settings.PG_MERCHANTID
    merchantUserId = settings.PG_MID
    merchantSalt = settings.PG_M_SALT_KEY
    phonepay_url = settings.PG_PAY_URL
    # redirect_to = host + str('/payment/create-phonerpay-order-link/')
    
    # callback_url = "https://webhook.site/de06884f-63bb-4c18-8f13-f9fe8b436391"
    # https://coursetube.in/payment/create-phonerpay-order-link/?amount=1&customer_name=Raj&customer_phone=9879879877&description=TestDescription&tnx_id=bgasdh

    serializer = CreatePaymentLinkSerialiser(data=request.GET)
    if not serializer.is_valid():
        return HttpResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)
    data = serializer.data
    tnx_id = data['tnx_id']
    redirect_to = host + str('/payment/webhook-phonepay/') + f"{tnx_id}/"
    # redirect_to = "https://coursetube.in/payment/create-phonerpay-order-link/"
    callback_url = redirect_to
    context = {
        "merchantId": merchantId,
        "merchantTransactionId": tnx_id,
        "merchantUserId": merchantUserId,
        "amount": int(data['amount']) * 100,
        "redirectMode": "REDIRECT",
        "redirectUrl": callback_url,
        "callbackUrl": redirect_to,
        "mobileNumber": data['customer_phone'],
        "paymentInstrument": {
            "type": "PAY_PAGE"
        }
    }
    
    """ base64 encoded context value of request_body """
    json_string = json.dumps(context)
    base64_encoded = base64.b64encode(json_string.encode('utf-8')).decode('utf-8')
    request_body = str(base64_encoded)

    """ sha256 online """
    sha_data = request_body + "/pg/v1/pay" + merchantSalt
    sha256_hash = hashlib.sha256()

    # Update the hash object with your data
    sha256_hash.update(sha_data.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hashed_data = sha256_hash.hexdigest()
    sha256 = hashed_data + "###" + "1"

    payload = json.dumps({
        "request": request_body
    })

    headers = {
        'Content-Type': 'application/json',
        'X-VERIFY': sha256,
        'accept': 'application/json'
    }

    pg_response = requests.post(url=phonepay_url, data=payload, headers=headers)
    if pg_response.status_code == 200:
        result = pg_response.json()
        pay_url = result['data']['instrumentResponse']['redirectInfo']['url']
        return render(request, "frontend/redirect.html", {"payurl": pay_url})

        # return_url = host + reverse('phonepay_webhook') + f'?ref={pay_url}'
        # return HttpResponseRedirect(pay_url)
        # return return_url
    
    return HttpResponse({"messsage": "Invaolid payload"}, status=pg_response.status_code)
    
    # except Exception as ex:
    #     return HttpResponse({"message": f"{ex}"}
    # )


def check_pg_transaction_status(request, tran_id):
    tran_id = int(tran_id)
    host = f"{request.scheme}://{request.META['HTTP_HOST']}"
    merchantId = settings.PG_MERCHANTID
    merchantUserId = settings.PG_MID
    merchantSalt = settings.PG_M_SALT_KEY

    frontend_url = os.environ.get("FRONTEND_URL")
    redirect_front = frontend_url + '/recharge/'
    try:

        # url = f"https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/{merchantId}/{tran_id}"
        url = f"https://mercury-t2.phonepe.com/v3/transaction/{merchantId}/{tran_id}/status"

        # for Sha256 calculation
        str_forSha256 = '/v3/transaction/' + merchantId + '/' + str(tran_id) + '/status' + merchantSalt
        sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()
        x_verify = sha_value + '###1'

        headers = {
            'Content-Type': 'application/json',
            'X-MERCHANT-ID': merchantId,
            'X-VERIFY': x_verify,
            'accept': 'application/json'
        }

        response = requests.get(url, headers=headers)
        result = response.json()
        if result['success']:
            if result['data']['payResponseCode'] == "SUCCESS":
                tnx_status = True
            else:
                tnx_status = False
        else:
            tnx_status = False
        
        # call payment api of frontend of success
        # frontend_url = "http://127.0.0.1:8080"
        frontend_webhook = frontend_url + '/webhook/phonepay/'
        webhook_res = requests.post(
            url=frontend_webhook, 
            data={
                "tnxid": tran_id,
                "success": tnx_status
            }
        )
        
    except Exception as ex:
        print(str(ex))
    finally:
        return redirect(redirect_front)
