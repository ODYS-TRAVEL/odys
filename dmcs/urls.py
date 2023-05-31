from rest_framework import routers

from dmcs.views import DMCView

router = routers.SimpleRouter()
router.register('', DMCView, basename='dmcs')

urlpatterns = router.urls + []
