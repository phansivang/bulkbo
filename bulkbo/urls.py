from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('login/',views.LoginView.as_view(),name='login' ),
    path('register/',views.registerview,name='register' ),
    path('',views.homepage,name='home'),
    path(f'config/sender-profile/', views.senderprofileview,name='senderconfig'),
    path('reports/',views.reportviews,name = 'report'),
    path('test/', TemplateView.as_view(template_name="test.html")),

]
