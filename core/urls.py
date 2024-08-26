from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('delete/', views.delete_all_data, name='delete_all_data'),
]
