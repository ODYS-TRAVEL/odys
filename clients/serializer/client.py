from rest_framework import serializers


class ClientSerializer(serializers.Serializer):
    client_id = serializers.CharField(max_length=100)  # ID
    name = serializers.CharField(max_length=100)  # NOM
    last_name = serializers.CharField(max_length=100)  # Prénom
    client_type = serializers.CharField(max_length=100)  # Type de client
    country = serializers.CharField(max_length=100)  # Pays
    
    def to_internal_value(self, data):
        return {
            'Num Dossier': data['client_id'],
            'NOM': data['name'],
            'Prénom': data['last_name'],
            'Type de client': data['client_type'],
            'Pays client': data['country'],
        }
