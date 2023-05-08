from rest_framework import routers

from bookings.views import BookingView

router = routers.SimpleRouter()
router.register('', BookingView, basename='bookings')


urlpatterns = router.urls + []
