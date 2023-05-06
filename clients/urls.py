from rest_framework import routers

from clients.views import ClientView


router = routers.SimpleRouter()
router.register('', ClientView, basename='clients')

urlpatterns = router.urls + [

]
