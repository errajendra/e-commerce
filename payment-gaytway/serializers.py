from rest_framework import serializers


class CreatePaymentLinkSerialiser(serializers.Serializer):
    amount = serializers.FloatField()
    description = serializers.CharField()
    tnx_id = serializers.CharField()
    customer_name = serializers.CharField()
    customer_email = serializers.CharField()
    customer_phone = serializers.CharField()
