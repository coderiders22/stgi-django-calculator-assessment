from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .models import CalculationHistory
from .serializers import CalculationHistorySerializer
from .authentication import CsrfExemptSessionAuthentication


# =========================
# CALCULATE
# =========================
class CalculateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        try:
            a = float(request.data.get("operand1"))
            b = float(request.data.get("operand2"))
            op = request.data.get("operator")
            note = request.data.get("note", "").strip()
        except Exception:
            return Response({"error": "Invalid input"}, status=400)

        if op not in ["+", "-", "*", "/"]:
            return Response({"error": "Invalid operator"}, status=400)

        if op == "/" and b == 0:
            return Response({"error": "Division by zero"}, status=400)

        result = eval(f"{a}{op}{b}")

        data = {
            "operand1": a,
            "operand2": b,
            "operator": op,
            "result": result,
            "note": note[:500]
        }

        if request.user.is_authenticated:
            data["user"] = request.user
        else:
            if not request.session.session_key:
                request.session.create()

            data["session_key"] = request.session.session_key

            if CalculationHistory.objects.filter(session_key=request.session.session_key).count() >= 10:
                return Response(
                    {"error": "Guest calculation limit reached"},
                    status=403
                )

        CalculationHistory.objects.create(**data)
        return Response({"result": result}, status=201)


# =========================
# HISTORY
# =========================
class HistoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            history = CalculationHistory.objects.filter(user=request.user)
        else:
            if not request.session.session_key:
                return Response([])
            history = CalculationHistory.objects.filter(session_key=request.session.session_key)

        serializer = CalculationHistorySerializer(history.order_by("-created_at"), many=True)
        return Response(serializer.data)


# =========================
# CLEAR HISTORY
# =========================
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
@authentication_classes([CsrfExemptSessionAuthentication])
def clear_history(request):
    CalculationHistory.objects.filter(user=request.user).delete()
    return Response({"detail": "History cleared"})


# =========================
# DELETE ITEM
# =========================
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
@authentication_classes([CsrfExemptSessionAuthentication])
def delete_history_item(request, pk):
    CalculationHistory.objects.filter(id=pk, user=request.user).delete()
    return Response({"detail": "Deleted"})
