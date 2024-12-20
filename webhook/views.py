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
