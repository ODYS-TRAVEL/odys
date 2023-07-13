from rest_framework import routers

from bookings.views import AgenciesBookingView

router = routers.SimpleRouter()
router.register('', AgenciesBookingView, basename='bookings')


urlpatterns = router.urls + []
