from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import AccountSerializer
from .models import Account
from users.models import User
from users.serializers import UserRegistrationSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.filter(isActive='Y').order_by('accountNumber')
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticated,)

    @action(methods=['post'], detail=True,
            url_path='closeAccount', url_name='closeAccount', permission_classes=[IsAdminUser])
    def close_account(self, request, pk):
        account = self.get_object()
        account.isActive = 'N'
        account.save()
        return Response({'status': 'account closed'})

    @action(methods=['post'], detail=False,
            url_path='openAccount', url_name='openAccount', permission_classes=[IsAdminUser])
    def open_account(self, request):
        user_json = request.data.pop('user')
        customer = None
        existing_user_id = 0
        if "id" in user_json:
            existing_user_id = user_json.pop('id')
        if existing_user_id != 0:
            customer = User.objects.get(id=existing_user_id)
        else:
            if "id" in user_json:
                del user_json['id']
            serializer = UserRegistrationSerializer(data=user_json)
            valid = serializer.is_valid(raise_exception=True)
            if valid:
                customer = serializer.save()
            else:
                return Response({'message': 'Something went wrong!'})
        account = Account.objects.create(user=customer, accountType=request.data.pop('accountType'),
                                         balance=request.data.pop('balance'), isActive='Y')
        response = {
                'message': 'Account added successfully!',
                'account': AccountSerializer(account).data
        }
        return Response(response)