from rest_framework import serializers


class ClientSerializer(serializers.Serializer):
    client_id = serializers.CharField(max_length=40)
    surname = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    dmc = serializers.CharField(max_length=100)
    client_profile = serializers.CharField(max_length=4000, required=False, allow_blank=True)
    country = serializers.CharField(max_length=100, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=100, required=False, allow_blank=True)
    email = serializers.CharField(max_length=100, required=False, allow_blank=True)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        client_id = data.pop('client_id')
        dmc = data.pop('dmc')
        data['dmc'] = [dmc]
        data['project'] = {
            'client_number': client_id,
            'client_profile': data.pop('client_profile'),
            'source': 'B2B',
        }
        return data
