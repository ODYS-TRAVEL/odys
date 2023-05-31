from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from services import airtable_service


class DMCView(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        dmcs = airtable_service.dmcs.operation('all')
        return Response([dict(id=dmc['id'], name=dmc['fields']['dmc_name']) for dmc in dmcs])
