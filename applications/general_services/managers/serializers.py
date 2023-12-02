from rest_framework import serializers


class EmailSerializer(serializers.Serializer):
    sender = serializers.EmailField(required=True)
    receipients = serializers.ListField(
        allow_empty=False,
        child=serializers.EmailField(required=True),
    )
    body = serializers.CharField(max_length=1000)