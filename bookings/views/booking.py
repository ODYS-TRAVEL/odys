import json
from requests.exceptions import HTTPError
from django.conf import settings
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bookings.serializer import BookingSerializer
from services import airtable_service


class BookingView(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            booking_data = BookingSerializer(data=request.data)
            booking_data.is_valid(raise_exception=True)
            client_data = booking_data.validated_data.pop('client')
            project_data = client_data.pop('project')
            project_data['agency_link'] = [request.user.agency.airtable_agency_id]
            project = airtable_service.projects.operation('create', project_data)
            client_data['project'] = [project['id']]
            client = airtable_service.clients.operation('create', client_data)
            client_id = client['id']
            booking_data.validated_data['client_link'] = [project['id']]
            booking = airtable_service.bookings.operation('create', booking_data.validated_data)
            bookind_id = booking['id']
        except HTTPError as e:
            return Response({'message': json.loads(e.response.text)}, status=e.response.status_code)
        return Response({'booking_id': bookind_id, 'client_id': client_id})
