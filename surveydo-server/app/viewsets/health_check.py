from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class HealthCheckViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    permission_classes = [AllowAny]

    def list(self, request):

        remote_address = request.META.get('REMOTE_ADDR')
        hostname = request.META.get('HOSTNAME')
        server_name = request.META.get('SERVER_NAME')
        server_port = request.META.get('SERVER_PORT')
        django_configuration = request.META.get('DJANGO_CONFIGURATION')
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        return Response({
            'remote_address': remote_address,
            'hostname': hostname,
            'server_name': server_name,
            'server_port': server_port,
            'django_configuration': django_configuration,
            'x_forwarded_for': x_forwarded_for
        })
