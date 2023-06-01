from datetime import datetime
from rest_framework import serializers

from clients.serializer import ClientSerializer


class ParticipantSerializer(serializers.Serializer):
    surname = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    birthday = serializers.DateField()


class BookingSerializer(serializers.Serializer):
    agency_booking_id = serializers.CharField(max_length=100)
    client_product_title_edit = serializers.CharField(max_length=400)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    departure_time_edit = serializers.CharField(
        max_length=5,
        required=False,
        allow_blank=True,
    )
    client_hotel = serializers.CharField(max_length=400, allow_null=True, required=False, allow_blank=True)
    meeting_point_edit = serializers.CharField(max_length=400, allow_null=True, required=False, allow_blank=True)
    arrival_point = serializers.CharField(max_length=400, allow_null=True, required=False, allow_blank=True)
    booking_details = serializers.CharField(max_length=400, allow_null=True, required=False, allow_blank=True)
    pax = serializers.IntegerField()
    participants = ParticipantSerializer(many=True)
    booking_options = serializers.CharField(max_length=400, allow_null=True, required=False, allow_blank=True)
    agent_emails = serializers.ListField(child=serializers.CharField(max_length=400))
    client = ClientSerializer()

    def validate_departure_time_edit(self, value):
        if not value:
            return value
        time_format = '%H:%M'
        try:
            parsed_time = datetime.strptime(value, time_format).time()
        except ValueError:
            raise serializers.ValidationError(f'Invalid time format. Use {time_format}')
        return parsed_time

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        departure_time = data.pop('departure_time_edit', None)
        if departure_time:
            departure_time_secs = departure_time.hour * 3600 + departure_time.minute * 60
            data['departure_time_edit'] = departure_time_secs

        participants = ''
        for participant in data['participants']:
            birthday = str(participant['birthday'])
            participants += f"- {participant['surname']} ; {participant['last_name']} ; {birthday}\n"

        data['participants'] = participants
        agent_emails = ', '.join(data.pop('agent_emails', []))
        data['client_email_edit'] = agent_emails
        data['start_date'] = str(data['start_date'])
        data['end_date'] = str(data['end_date'])
        data['operation_status'] = 'Revision pending'
        return data
