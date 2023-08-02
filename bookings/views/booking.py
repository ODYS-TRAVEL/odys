import json
from requests.exceptions import HTTPError
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bookings.serializer import BookingSerializer, AirtableBookingSerializer
from services import airtable_service

from clients.views import ClientMixin


class ClientsBookingView(ViewSet, ClientMixin):
    permission_classes = [IsAuthenticated]

    def create(self, request, **kwargs):
        try:
            client = self.get_client(kwargs['client_odys_client_id'])
            project_id = client['fields']['project'][0]
            booking_data = BookingSerializer(data=request.data)
            booking_data.is_valid(raise_exception=True)
            booking_data.validated_data['client_link'] = [project_id]
            booking = airtable_service.bookings.operation('create', booking_data.validated_data)
            bookind_id = booking['id']
            return Response({'booking_id': bookind_id})
        except HTTPError as e:
            return Response({'message': json.loads(e.response.text)}, status=e.response.status_code)


class AgenciesBookingView(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer = AirtableBookingSerializer

    def retrieve(self, request, pk=None, **kwargs):
        agency_id = request.user.agency.airtable_agency_id
        agency = airtable_service.agencies.operation('get', agency_id)
        agency_name = agency['fields']['agency']
        formula = f'AND(agency_booking_id = "{pk}", client_type = "{agency_name}", hidden_service = "")'
        bookings = airtable_service.bookings.operation('all', formula=formula)
        serialized_data = self.serializer(data=[b['fields'] for b in bookings], many=True)
        serialized_data.is_valid(raise_exception=True)
        return Response(self.serializer.from_airtable_to_api(serialized_data.data))
