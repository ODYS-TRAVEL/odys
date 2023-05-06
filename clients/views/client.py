from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class ClientView(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        return Response({'message': 'created'})
