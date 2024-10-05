from django.contrib import admin
from django.urls import include, path
from django.urls import path


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
    
    # path('pages/sign-in/', views.sign_in, name='sign_in'),
    # path('pages/dashboard/', views.dashboard, name='dashboard'),
    # path('pages/tables/', views.tables, name='tables'),
    # path('pages/billing/', views.billing, name='billing'),
    # path('pages/virtual-reality/', views.virtual_reality, name='virtual_reality'),
    # path('pages/notifications/', views.notifications, name='notifications'),
    # path('pages/profile/', views.profile, name='profile'),
    # path('pages/sign-up/', views.sigh_up, name='sigh_up'),
]

