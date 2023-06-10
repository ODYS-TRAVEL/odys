import json
from requests.exceptions import HTTPError
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bookings.serializer import BookingSerializer
from services import airtable_service

from clients.views import ClientMixin


class BookingView(ViewSet, ClientMixin):
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
