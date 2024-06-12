from django.urls import path
from django.urls import path, include
from rest_framework import routers
from .views import ClientViewSet, ProjectViewSet

router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('clients/<int:client_id>/projects/', ProjectViewSet.as_view({'post': 'create'}), name='client-projects'),
]
