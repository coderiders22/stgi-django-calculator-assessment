from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes

from .models import CalculationHistory
from .serializers import CalculationHistorySerializer


# =========================
# CALCULATE API
# =========================
class CalculateView(APIView):
    permission_classes = [AllowAny]  # guest can calculate

    def post(self, request):
        try:
            a = float(request.data.get("operand1"))
            b = float(request.data.get("operand2"))
            op = request.data.get("operator")
            note = request.data.get("note", "").strip()  # Get optional note
        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid number input"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if op not in ["+", "-", "*", "/"]:
            return Response(
                {"error": "Invalid operator"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ SAFE CALCULATION
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            if b == 0:
                return Response(
                    {"error": "Division by zero not allowed"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            result = a / b

        data = {
            "operand1": a,
            "operand2": b,
            "operator": op,
            "result": result,
            "note": note[:500]  # Limit to 500 characters
        }

        # AUTH USER → USER HISTORY (Unlimited notes)
        if request.user.is_authenticated:
            data["user"] = request.user

        # GUEST → SESSION HISTORY (LIMITED)
        else:
            if not request.session.session_key:
                request.session.create()

            data["session_key"] = request.session.session_key

            # Guest history limit (10 calculations)
            guest_count = CalculationHistory.objects.filter(
                session_key=request.session.session_key
            ).count()

            if guest_count >= 10:
                return Response(
                    {
                        "error": "Guest calculation limit reached. Log in to unlock full access."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Guest notes limit (Only 2 calculations can have notes)
            if note:  # If guest is trying to add a note
                guest_notes_count = CalculationHistory.objects.filter(
                    session_key=request.session.session_key
                ).exclude(note='').count()
                
                if guest_notes_count >= 2:
                    return Response(
                        {
                            "error": "Guest note limit reached. You can only add notes to 2 calculations. Login for unlimited notes."
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )

        CalculationHistory.objects.create(**data)

        return Response(
            {"saved": True, "result": result},
            status=status.HTTP_201_CREATED
        )


# =========================
# FETCH HISTORY (USER + GUEST)
# =========================
class HistoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            # Order by newest first for authenticated users
            history = CalculationHistory.objects.filter(
                user=request.user
            ).order_by('-created_at')

        else:
            if not request.session.session_key:
                return Response([], status=status.HTTP_200_OK)

            # Order by newest first and limit to 10 for guests
            history = CalculationHistory.objects.filter(
                session_key=request.session.session_key
            ).order_by('-created_at')[:10]

        serializer = CalculationHistorySerializer(history, many=True)
        return Response(serializer.data)


# =========================
# CLEAR ALL HISTORY (AUTH ONLY)
# =========================
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def clear_history(request):
    CalculationHistory.objects.filter(user=request.user).delete()

    return Response(
        {"detail": "History cleared successfully"},
        status=status.HTTP_200_OK
    )


# =========================
# DELETE SINGLE HISTORY ITEM (AUTH ONLY)
# =========================
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_history_item(request, pk):
    try:
        item = CalculationHistory.objects.get(id=pk, user=request.user)
    except CalculationHistory.DoesNotExist:
        return Response(
            {"detail": "History item not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    item.delete()

    return Response(
        {"detail": "History item deleted"},
        status=status.HTTP_200_OK
    )