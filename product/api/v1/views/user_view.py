from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.v1.permissions import IsStaff  # NEW
from users.models import Balance  # NEW
from api.v1.serializers.user_serializer import CustomUserSerializer, BalanceSerializer  # NEW

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ["get", "head", "options"]
    permission_classes = (permissions.IsAdminUser,)


# NEW start
class BalanceViewSet(viewsets.GenericViewSet):
    serializer_class = BalanceSerializer

    # получаем экземпляр баланса по id пользователя
    def get_object(self):
        user_id = self.kwargs.get('pk')
        return get_object_or_404(Balance, user_id=user_id)

    @action(detail=True, methods=["post"], permission_classes=[IsStaff])
    def add_amount(self, request, pk=None):
        """Начисление баланса - бонусов"""
        balance = self.get_object()
        amount = request.data["amount"]
        serializer = self.get_serializer(balance, self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        balance.amount += int(amount)
        balance.save()
        return Response(
            data={
                "status": "success",
                "amount": balance.amount
            },
            status=status.HTTP_200_OK
        )
# NEW end
