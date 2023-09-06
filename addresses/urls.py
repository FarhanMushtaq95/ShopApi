from django.urls import path

from addresses.views import AddressListView
from products.views import ProductListView, ProductDetailsView

app_name = 'addresses'
urlpatterns = [
    path('users/addresses/', AddressListView.as_view(), name='address_list'),
]
