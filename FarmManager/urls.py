from django.contrib import admin
from django.urls import include, path
from django.urls import path
from .views import ReportHeatSignView
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'farms', views.FarmViewSet)
router.register(r'cows', views.CowViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.dashboard),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tables/', views.tables, name='tables'),
    path('notifications/', views.notifications, name='notifications'),   
    path('search_farm/', views.search_farm, name='search_farm'),
    path('search_animal/', views.search_animal, name='search_animal'),
    path('trigger/', views.trigger_alerts, name='triger'),
    path('average-statistics/', views.average_statistics, name='average_statistics'),
    path('receive-data/', views.receive_data, name='receive_data'),
    path('api/', include(router.urls)),
    path('api/statistics/', views.average_statistics, name='average_statistics'),
]

