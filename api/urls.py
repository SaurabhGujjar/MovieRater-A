from django.urls import path, include
from .views import MovieViewSet, RatingViewSet, UserViewSet
from rest_framework import routers
router = routers.DefaultRouter()
router.register('movies', MovieViewSet)
router.register('ratings', RatingViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
]



