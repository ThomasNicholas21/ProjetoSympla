from rest_framework import serializers
from logs.models import Log


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = [
            'id', 'batch', 'message',
            'imported_amount', 'status',
            'created_at'
        ]
