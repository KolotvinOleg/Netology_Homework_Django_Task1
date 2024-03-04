from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.serializers import AdvertisementSerializer
from .models import Advertisement
from .permissions import IsOwner


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = AdvertisementFilter
    filterset_filds = ['created_at', 'status', 'creator']

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == "create":
            return [IsAuthenticated()]
        if self.action in ["destroy", "update", "partial_update"]:
            return [IsAuthenticated(), IsOwner()]
        return []
