from django.contrib import admin
from django.urls import include, path
from django.urls import path
from .views import ReportHeatSignView


from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('myapp.urls')),
    # path('',views.dashboard),
    path('',views.sign_in),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tables/', views.tables, name='tables'),
    path('billing/', views.billing, name='billing'),
    path('virtual-reality/', views.virtual_reality, name='virtual_reality'),
    path('rtl/', views.rtl, name='rtl'),
    path('notifications/', views.notifications, name='notifications'),
    # path('profile/', views.profile, name='profile'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('sign-up/', views.sign_up, name='sign_up'),
    # path('farm-details/', views.farm_details, name='farm_details'),
    path('api/report-heat-sign/<str:cow_id>/', ReportHeatSignView.as_view(), name='report-heat-sign'),
    path('search_farm/', views.search_farm, name='search_farm'),
    path('search_animal/', views.search_animal, name='search_animal'),

    # path('pages/sign-in/', views.sign_in, name='sign_in'),
    # path('pages/dashboard/', views.dashboard, name='dashboard'),
    # path('pages/tables/', views.tables, name='tables'),
    # path('pages/billing/', views.billing, name='billing'),
    # path('pages/virtual-reality/', views.virtual_reality, name='virtual_reality'),
    # path('pages/notifications/', views.notifications, name='notifications'),
    # path('pages/profile/', views.profile, name='profile'),
    # path('pages/sign-up/', views.sigh_up, name='sigh_up'),
]

