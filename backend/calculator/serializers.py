# calculator/serializers.py

from rest_framework import serializers
from .models import CalculationHistory


class CalculationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CalculationHistory
        fields = [
            'id',
            'user',
            'session_key',
            'operand1',
            'operand2',
            'operator',
            'result',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']