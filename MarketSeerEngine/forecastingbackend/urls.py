from django.urls import path
from . import marketseer_api, views

urlpatterns = [
	path('data/', marketseer_api.datarequest, name='datarequest'),
	path('', views.index, name='index'),
]
