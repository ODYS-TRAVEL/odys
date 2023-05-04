from rest_framework import serializers


class ClientSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)  # NOM
    last_name = serializers.CharField(max_length=100)  # Prénom
    client_type = serializers.CharField(max_length=100)  # Type de client
    country = serializers.CharField(max_length=100)  # Pays
    
