from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from clients.views import ClientView
from bookings.views import ClientsBookingView

client_router = routers.SimpleRouter()
client_router.register('clients', ClientView, basename='clients')

bookings_router = nested_routers.NestedSimpleRouter(client_router, r'clients', lookup='client')
bookings_router.register('bookings', ClientsBookingView, basename='bookings')


urlpatterns = client_router.urls + bookings_router.urls
