from rest_framework import serializers, fields

from daewoobuss.models import BusStations



class DaewooBussSerializer(serializers.ModelSerializer):


    class Meta:
        model = BusStations
        fields = ['id', 'terminal_name', 'terminal_code']
