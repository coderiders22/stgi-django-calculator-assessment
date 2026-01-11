# calculator/serializers.py

from rest_framework import serializers
from .models import CalculationHistory


class CalculationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CalculationHistory
        fields = [
            "id",
            "operand1",
            "operand2",
            "operator",
            "result",
            "note",       
            "created_at",
        ]
        read_only_fields = ['id', 'created_at']