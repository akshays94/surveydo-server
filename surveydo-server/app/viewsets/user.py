from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from ..models import User
from ..permissions import IsUserOrReadOnly
from ..serializers.user import CreateUserSerializer
from ..serializers.user import UserSerializer



class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)


class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Creates user accounts
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.pk,
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
        # docker exec -it surveydo-server_postgres_1 psql -U postgres -d postgres

class LogoutViewSet(viewsets.GenericViewSet):

    @action(url_path='validate-token', detail=False, methods=['get'])
    def validate_token(self, request, format=None):
        return Response(status=status.HTTP_200_OK)

    @action(url_path='logout', detail=False, methods=['post'])
    def logout_user(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
