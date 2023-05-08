from rest_framework import serializers

from clients.serializer import ClientSerializer


class ParticipantSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    birthday = serializers.DateField()


class BookingSerializer(serializers.Serializer):
    booking_id = serializers.CharField(max_length=100)
    product_name = serializers.CharField(max_length=400)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    departure_time = serializers.TimeField(input_formats=['%H:%M'], required=False)
    client_hotel = serializers.CharField(max_length=400, allow_null=True, required=False)
    meetting_point = serializers.CharField(max_length=400, allow_null=True, required=False)
    arrival_point = serializers.CharField(max_length=400, allow_null=True, required=False)
    booking_details = serializers.CharField(max_length=400, allow_null=True, required=False)
    pax = serializers.IntegerField()
    participants = ParticipantSerializer(many=True)
    booking_options = serializers.CharField(max_length=400, allow_null=True, required=False)
    email = serializers.CharField(max_length=400)
    client = ClientSerializer()


    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        departure_time = data.get('departure_time', '')
        if departure_time:
            departure_time_secs = departure_time.hour * 3600 + departure_time.minute * 60

        participants = ''
        for participant in data['participants']:
            birthday = str(participant['birthday'])
            participants += f"- {participant['name']} ; {participant['last_name']} ; {birthday}\n"

        return {
            'Agency booking ID':  data['booking_id'],
            'Product Name for client':  data['product_name'],
            'Start Date':  str(data['start_date']),
            'End date':  str(data['end_date']),
            'Departure time':  departure_time_secs,
            "Client's hotel":  data.get('client_hotel', ''),
            'Meeting point': data.get('meetting_point', ''),
            'Arrival Point': data.get('arrival_point', ''),
            'Operation Status': 'Revision pending',
            'Booking Details from Agency': data.get('booking_details', ''),
            'Pax': data['pax'],
            'Participants': participants,
            'Booking Options': data.get('booking_options', ''),
            'email': data['email'],
            'client': data['client'],
        }

