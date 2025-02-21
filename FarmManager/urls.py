from django.contrib import admin
from django.urls import include, path
from django.urls import path
from .views import FarmViewSet, CowViewSet, MessageViewSet, InseminatorViewSet
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'farms', FarmViewSet)
router.register(r'cows', CowViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'inseminators', InseminatorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
