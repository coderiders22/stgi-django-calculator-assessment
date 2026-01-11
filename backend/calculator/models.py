# calculator/models.py
from django.db import models
from django.conf import settings


class CalculationHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,         
        blank=True,
        related_name='calculations'
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)  # for guest
    operand1 = models.FloatField()
    operand2 = models.FloatField()
    operator = models.CharField(max_length=1)
    result = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.operand1} {self.operator} {self.operand2} = {self.result}"