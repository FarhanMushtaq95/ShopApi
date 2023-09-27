from django.urls import path

from daewoobuss.views import DataInsertion, BussStationListView, BussRouteView, BussTicketBooking

app_name = 'daewoobuss'
urlpatterns = [
    path('dbfill', DataInsertion.as_view(), name='data_insert'),
    path('daewoo/getstations/', BussStationListView.as_view(), name='buss_get'),
    path('daewoo/getroutes/', BussRouteView.as_view(), name='buss_route_get'),
    path('daewoo/seatBooking/', BussTicketBooking.as_view(), name='buss_booking'),


]
