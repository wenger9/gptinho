from django.apps import AppConfig


class DataAssetsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "data_assets"


#from django.urls import path
#from . import views

#urlpatterns = [
#    path('', views.data_assets_list, name='data_assets_list'),
#    path('<int:pk>/', views.data_asset_detail, name='data_asset_detail'),
#]

