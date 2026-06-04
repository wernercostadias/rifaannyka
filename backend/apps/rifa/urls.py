from rest_framework.routers import DefaultRouter

from .views import RaffleViewSet


router = DefaultRouter()
router.register("raffles", RaffleViewSet, basename="raffle")

urlpatterns = router.urls
