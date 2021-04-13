from django.urls import path

from . import views

app_name = 'DisplayApp'

urlpatterns = [
    path(r'', views.index, name='index'),
]