import requests
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreatePaymentLinkSerialiser


def redirect_payment_url(request):
    payurl = request.GET.get('ref', '')
    return render(request, "frontend/redirect.html", {"payurl": payurl})


def get_payu_access_token():
    # UAT
    url = settings.PAYU_AUTH_URL
    client_id = settings.PAYU_CLIENT_ID
    client_secret = settings.PAYU_SECRET_KEY
    
    payload = {
        "grant_type": "client_credentials",
        "scope": "create_payment_links",
        "client_id": client_id,
        "client_secret": client_secret
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=payload, headers=headers)
    token = response.json()['access_token'] if response.status_code == 200 else None
    return token


@csrf_exempt
@api_view(['post'])
def create_payu_order_link(request):
    print(request.data)
    serializer = CreatePaymentLinkSerialiser(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    data = serializer.data
    access_token = get_payu_access_token()
    if access_token:
        url = settings.PAYU_PAYLINK_URL
        payload = {
            "subAmount": data['amount'],
            "isPartialPaymentAllowed": False,
            "description": data['description'],
            "source": "API",
            "customer": {
                "name": data['customer_name'],
                "email": data['customer_email'],
                "email": data['customer_email'],
                "phone": data['customer_phone']
            },
            "transactionId": data['tnx_id'],
        }

        headers = {
            "accept": "application/json",
            "mid": f"{settings.PAYU_MID}",
            "content-type": "application/json",
            "authorization": f"Bearer {access_token}"
        }
        response = requests.post(url, json=payload, headers=headers)
        print(response.json())
        return Response(response.json(), response.status_code)
    
    return Response(
        data = {"message": "Invalid access token"}, 
        status = status.HTTP_500_INTERNAL_SERVER_ERROR
    )
