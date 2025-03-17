from rest_framework import serializers


EXCLUDED_TIME_FIELDS = [
    "created_at",
    "updated_at",
    "is_deleted",
    "deleted_at",
]


class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField(max_length=300)
