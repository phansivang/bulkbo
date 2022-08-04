from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.LoginView.as_view(),name='login' ),
    path('register/',views.registerview,name='register' ),
    path('',views.homepage,name='home'),
    path(f'config/sender-profile/', views.senderprofileview,name='senderconfig'),
    path('reports/',views.reportviews,name = 'report')

]
