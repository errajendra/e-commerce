import requests
from django.shortcuts import render
from django.http import HttpResponse
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



def payment_successful(request):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Payment Successful</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f8ff;
                color: #333;
                text-align: center;
                padding: 50px;
            }
            .success-message {
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
                color: #155724;
                padding: 20px;
                border-radius: 5px;
                display: inline-block;
            }
            .button {
                margin-top: 20px;
                padding: 10px 20px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .button:hover {
                background-color: #0056b3;
            }
        </style>
        <script>
            // Prevent back navigation
            history.pushState(null, document.title, location.href);
            window.addEventListener('popstate', function(event) {
                history.pushState(null, document.title, location.href);
            });
        </script>
    </head>
    <body>

        <div class="success-message">
            <h1>Payment Successful!</h1>
            <p>Thank you for your payment. Your transaction has been completed successfully.</p>
            <p>You will receive a confirmation email shortly.</p>
            <button class="button" onclick="window.close();">Close this Page</button>
        </div>

    </body>
    </html>
    """
    
    # Set headers to prevent caching
    response = HttpResponse(html_content)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response


def payment_failed(request):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Payment Failed</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f8d7da;
                color: #721c24;
                text-align: center;
                padding: 50px;
            }
            .error-message {
                background-color: #f5c6cb;
                border: 1px solid #f5c6cb;
                color: #721c24;
                padding: 20px;
                border-radius: 5px;
                display: inline-block;
            }
            .button {
                margin-top: 20px;
                padding: 10px 20px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .button:hover {
                background-color: #0056b3;
            }
        </style>
        <script>
            // Prevent back navigation
            history.pushState(null, document.title, location.href);
            window.addEventListener('popstate', function(event) {
                history.pushState(null, document.title, location.href);
            });
        </script>
    </head>
    <body>

        <div class="error-message">
            <h1>Payment Failed!</h1>
            <p>We're sorry, but your payment could not be processed.</p>
            <p>Please check your payment details and try again.</p>
            <button class="button" onclick="window.history.back();">Try Again</button>
        </div>

    </body>
    </html>
    """
    # Set headers to prevent caching
    response = HttpResponse(html_content)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response
