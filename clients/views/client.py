import json
from requests.exceptions import HTTPError
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from clients.serializer import ClientSerializer
from services import airtable_service, catch_airtable_error

class ClientMixin():
    def get_client(self, odys_client_id):
        return airtable_service.clients.operation('get', odys_client_id)

    def already_exists(self, odys_client_id, airtable_agency_id):
        formula = f'AND(client_number = "{odys_client_id}", FIND("{airtable_agency_id}", agency_link))'
        return airtable_service.projects.operation('first', formula=formula)


class ClientView(ViewSet, ClientMixin):
    permission_classes = [IsAuthenticated]
    lookup_field = 'odys_client_id'

    def get_object(self, odys_client_id):
        return self.get_client(odys_client_id)

    @catch_airtable_error
    def create(self, request):
        client_data = ClientSerializer(data=request.data)
        client_data.is_valid(raise_exception=True)
        client_data = client_data.validated_data
        project_data = client_data.pop('project')
        existing_client = self.already_exists(project_data['client_number'], request.user.agency.airtable_agency_id)
        if existing_client:
            return Response({'client_id': existing_client['id']})
        project_data['agency_link'] = [request.user.agency.airtable_agency_id]
        project = airtable_service.projects.operation('create', project_data)
        client_data['project'] = [project['id']]
        client = airtable_service.clients.operation('create', client_data)
        client_id = client['id']
        return Response({'client_id': client_id})
