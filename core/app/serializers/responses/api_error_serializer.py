from rest_framework import serializers


class APIErrorSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        return data

    detail = serializers.CharField(
        help_text="Detailed information on the operation error."
    )
