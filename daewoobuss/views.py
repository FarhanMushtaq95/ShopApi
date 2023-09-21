from rest_framework.views import APIView
import requests
from daewoobuss.dbfill import datafill
from daewoobuss.models import BusStations
from rest_framework import generics, status
from rest_framework.response import Response
from shared.renderers import AppJsonRenderer
from daewoobuss.serializers import DaewooBussSerializer
# same as extending from generics.ListAPIView, generics.CreateAPIView
from users.authentication import IsAdminOrReadOnly
# Create your views here.


class DataInsertion(APIView):
    def get(self, request):
        data = datafill()
        return Response(data, status=200)


class BussStationListView(generics.ListCreateAPIView):
    queryset = BusStations.objects.all()
    serializer_class = DaewooBussSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        queryset = self.queryset.order_by('terminal_name')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BussRouteView(APIView):
    def get(self,request):
        # Get query parameters from the request
        departure_id = request.query_params.get('departureID')
        arrival_id = request.query_params.get('arrivalID')
        departure_date = request.query_params.get('departureDate')

        # Make a request to the external API
        url = f"https://testapi.daewoo.net.pk/api/schedule/getOfferedBusses?departureID={departure_id}&arrivalID={arrival_id}&departureDate={departure_date}"
        headers = {
            "x-client_id": "DES-0000",  # Replace with your actual client ID
            "x-client_password": "$desTination71024021"
        }

        response = requests.get(url, headers=headers)

        # Check if the request to the external API was successful
        if response.status_code == 200:
            external_data = response.json()


            return Response({
                "Data": external_data["Data"]
            })
        else:
            return Response({'error': 'Failed to fetch data from the external API'}, status=response.status_code)