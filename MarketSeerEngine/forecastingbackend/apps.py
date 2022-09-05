from django.apps import AppConfig
from forecastingbackend.global_data import ingest_stock_info_data

class ForecastingbackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forecastingbackend'

    def ready(self):
        ingest_stock_info_data()