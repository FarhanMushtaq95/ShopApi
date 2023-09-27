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
from django.http import JsonResponse
# Create your views here.
"""
{
            "RESERVATIONDATE": "20230929",
            "SCHEDULE_CODE": "1965734",
            "DEPARTURE_SEQ": "1",
            "ARRIVAL_SEQ": "4",
            "SCHEDULE_ROUTE": "16755",
            "SCHEDULE_ROUTE_NAME": "LHR-RWP-SHM-AFC-ABT",
            "SCHEDULE_DEPARTURE_TIME": "0600",
            "SCHEDULE_ARRIVAL_TIME": "1220",
            "SCHEDULE_TIMECODE": "1",
            "FARE_FARE": "2580",
            "FARE_Y": "0",
            "BUSTYPE_NAME": "D-45",
            "BUSTYPE_SEATS": "45",
            "STAFF_SEAT": "2",
            "AVAILABLE": "43",
            "TRIP_STATUS": "OK",
            "SCHEDULE_BUSTYPE": "12",
            "BUS_VIA": " "
        },
"""
class BussTicketBooking(APIView):
    def post(self, request, format=None):
        try:
            # Step 1: Obtain CLIENT_TOKEN
            url_token = "https://daewootestapi.daewoo.net.pk/api/secureplatform/token/getToken"
            headers_token = {
                "x-client_id": "DES-0000",
                "x-client_password": "$desTination71024021",
                "x-client_key": "testDestination71024021"
            }

            response_token = requests.get(url_token, headers=headers_token)
            response_token.raise_for_status()  # Raise HTTPError for bad responses
            client_token = response_token.json().get('CLIENT_TOKEN')

            if not client_token:
                return Response({'error': 'Unable to obtain CLIENT_TOKEN'}, status=status.HTTP_400_BAD_REQUEST)

            # Step 2: Use CLIENT_TOKEN to make the main API request
            url_main_api = "https://daewootestapi.daewoo.net.pk/api/booking/bookSeat"  # Replace with your actual main API endpoint
            headers_main_api = {
                "x-client_id": "DES-0000",
                "x-client_password": "$desTination71024021",
                "x-client-token": client_token
            }

            payload = request.data # Use the payload from the request body
            payload["CLIENT_TOKEN"] = client_token
            response_main_api = requests.post(url_main_api, json=payload, headers=headers_main_api)
            response_main_api.raise_for_status()  # Raise HTTPError for bad responses

            if response_main_api.status_code == 200:
                return Response(response_main_api.json(), status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to make main API request'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Error making API request: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': f'An unexpected error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


class DetailBookingView(APIView):
    def get(self,request):
        # Get query parameters from the request
        booking_date = request.query_params.get('bookingDate')
        booking_mobile_no = request.query_params.get('bookingMobileNo')
        booking_no = request.query_params.get('bookingNo')

        # Make a request to the external API
        url = f"https://daewootestapi.daewoo.net.pk/api/booking/getBookingDetails?bookingDate={booking_date}&bookingMobileNo={booking_mobile_no}&bookingNo={booking_no}"
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

class CancleBookingView(APIView):
    def get(self,request):
        # Get query parameters from the request
        booking_date = request.query_params.get('bookingDate')
        booking_mobile_no = request.query_params.get('bookingMobileNo')
        booking_no = request.query_params.get('bookingNo')

        # Make a request to the external API
        url = f"https://daewootestapi.daewoo.net.pk/api/booking/cancelBooking?bookingDate={booking_date}&bookingMobileNo={booking_mobile_no}&bookingNo={booking_no}"
        headers = {
            "x-client_id": "DES-0000",  # Replace with your actual client ID
            "x-client_password": "$desTination71024021"
        }

        response = requests.post(url, headers=headers)

        # Check if the request to the external API was successful
        if response.status_code == 200:
            external_data = response.json()


            return Response({
                "Data": external_data
            })
        else:
            return Response({'error': 'Failed to fetch data from the external API'}, status=response.status_code)