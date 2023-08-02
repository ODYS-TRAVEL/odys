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


class BookingImagesSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=1000)


class AirtableBookingSerializer(serializers.Serializer):
    names_changer = {
        'client_product_title_edit': 'product_title',
        'departure_time_edit': 'departure_time',
        'meeting_point_edit': 'meeting_point',
        'operation_status': 'status',
        'description_fr_edit': 'description_fr',
        'city_destination': 'city',
        'duration_edit': 'duration',
        'bring_edit': 'bring',
        'included_edit': 'included',
        'total_selling_price_usd_edit': 'total_price_usd',
        'comment_for_travelers': 'road_book_info',
        'dmc_comment_for_agency': 'comment_from_dmc',
    }

    agency_booking_id = serializers.CharField(max_length=100)
    client_product_title_edit = serializers.CharField(max_length=400)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    departure_time_edit = serializers.CharField(max_length=5, allow_null=True, required=False, allow_blank=True, default='')
    meeting_point_edit = serializers.CharField(max_length=400, allow_null=True, required=False, allow_blank=True, default='')
    arrival_point = serializers.CharField(max_length=400, allow_null=True, required=False, allow_blank=True, default='')
    operation_status = serializers.CharField(max_length=100)
    pax = serializers.IntegerField()
    participants = serializers.CharField(max_length=1000)
    description_fr_edit = serializers.CharField(max_length=1000, required=False, allow_blank=True, default='')
    hotel_description_fr = serializers.CharField(max_length=1000, required=False, allow_blank=True, default='')
    city_destination = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    duration_edit = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    bring_edit = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    included_edit = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    checkin_checkout = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    number_nights = serializers.IntegerField()
    supplier_booking_number = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    breakfast = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    breakfast_hour = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    transfer_distance = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    number_days_renta = serializers.IntegerField(required=False)
    total_selling_price_usd_edit = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    comment_for_travelers = serializers.CharField(max_length=1000, required=False, allow_blank=True, default='')
    dmc_comment_for_agency = serializers.CharField(max_length=1000, required=False, allow_blank=True, default='')
    images = BookingImagesSerializer(many=True, required=False, default=[])


    @classmethod
    def change_names(cls, data):
        for key, value in cls.names_changer.items():
            data[value] = data.pop(key)

    @classmethod
    def from_airtable_to_api(cls, data):
        if isinstance(data, list):
            for booking in data:
                cls.change_names(booking)
        else:
            cls.change_names(data)
        return data

    def validate_departure_time_edit(self, value):
        if not value:
            return ''
        return datetime.fromtimestamp(int(value)).strftime('%H:%M')
