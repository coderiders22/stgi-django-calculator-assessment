from django.contrib import admin
from .models import CalculationHistory


@admin.register(CalculationHistory)
class CalculationHistoryAdmin(admin.ModelAdmin):
    # admin can SEE
    list_display = (
        "id",
        "user",
        "session_key",
        "operand1",
        "operator",
        "operand2",
        "result",
        "created_at",
    )

    #  Filters & search (read-only safe)
    list_filter = ("operator", "created_at")
    search_fields = ("user__username", "session_key")

    #  Ordering
    ordering = ("-created_at",)

    #  Make EVERYTHING read-only
    readonly_fields = (
        "user",
        "session_key",
        "operand1",
        "operator",
        "operand2",
        "result",
        "created_at",
    )

    # Disable add
    def has_add_permission(self, request):
        return False

    # Disable delete
    def has_delete_permission(self, request, obj=None):
        return False

    # Disable edit
    def has_change_permission(self, request, obj=None):
        return False
