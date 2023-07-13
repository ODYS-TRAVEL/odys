import json
from requests.exceptions import HTTPError
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bookings.serializer import BookingSerializer
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

    def deserialize(self, airtable_booking):
        images = []
        for img in airtable_booking['fields'].get('images', []):
            images.append(img['url'])
        fields = [
            'agency_booking_id',
            'client_product_title_edit',
            'start_date',
            'end_date',
            'departure_time_edit',
            'meeting_point_edit',
            'arrival_point',
            'operation_status',
            'pax',
            'participants',
            'description_fr_edit',
            'hotel_description_fr',
            'city',
            'duration_edit',
            'bring_edit',
            'included_edit',
            'checkin_checkout',
            'number_nights',
            'supplier_booking_number',
            'breakfast',
            'breakfast_hour',
            'transfer_distance',
            'number_days_rental'
        ]
        booking = {field: airtable_booking['fields'].get(field, '') for field in fields}
        booking['images'] = images
        return booking

    def retrieve(self, request, pk=None, **kwargs):
        agency_id = request.user.agency.airtable_agency_id
        agency = airtable_service.agencies.operation('get', agency_id)
        agency_name = agency['fields']['agency']
        formula = f'AND(agency_booking_id = "{pk}", client_type = "{agency_name}", hidden_service = "")'
        bookings = airtable_service.bookings.operation('all', formula=formula)
        response = [self.deserialize(booking) for booking in bookings]
        return Response(response)
