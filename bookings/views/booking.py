import json
from requests.exceptions import HTTPError
from django.conf import settings
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bookings.serializer import BookingSerializer
from services import AirtableBase


class BookingView(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            booking_data = BookingSerializer(data=request.data)
            booking_data.is_valid(raise_exception=True)
            client_data = booking_data.validated_data.pop('client')
            client_data['LINK Agency'] = [request.user.agency.airtable_agency_id]
            airtable = AirtableBase(settings.AIRTABLE_API_TOKEN, settings.AIRTABLE_BASE_ID)
            client = airtable.clients.operation('create', client_data)
            client_id = client['id']
            booking_data.validated_data['LINK Client'] = [client_id]
            booking = airtable.bookings.operation('create', booking_data.validated_data)
            bookind_id = booking['id']
        except HTTPError as e:
            return Response({'message': json.loads(e.response.text)}, status=e.response.status_code)
        return Response({'booking_id': bookind_id, 'client_id': client_id})
