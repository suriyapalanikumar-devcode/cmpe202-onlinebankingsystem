from decimal import Decimal

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import PayeeSerializer
from .models import Payee
from accounts.models import Account
from rest_framework.fields import CurrentUserDefault


class PayeeViewSet(viewsets.ModelViewSet):
    queryset = Payee.objects.filter().order_by('id')
    serializer_class = PayeeSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    @action(methods=['post'], detail=False, url_path='add', url_name='add', permission_classes=[IsAuthenticated])
    def add(self, request):
        account = Account.objects.filter(accountNumber=request.data.pop('account')).first()
        payee = Payee.objects.create(user=self.request.user, account=account, **request.data)
        payee.save()
        response = {
            'message': 'Payee added successfully!',
            'payee': PayeeSerializer(payee).data
        }
        return Response(response)

    @action(methods=['get'], detail=False, url_path='get', url_name='get', permission_classes=[IsAuthenticated])
    def get_payees(self, request):
        payees = Payee.objects.filter(user=self.request.user)
        return Response(PayeeSerializer(payees, many=True).data)

    @action(methods=['post'], detail=True,
            url_path='delete', url_name='delete', permission_classes=[IsAuthenticated])
    def delete_payee(self, request, pk):
        payee = self.get_object()
        if payee.user.id == self.request.user.id:
            payee.delete()
        else:
            return Response({'status': 'Not allowed'})
        return Response({'status': 'payee deleted'})