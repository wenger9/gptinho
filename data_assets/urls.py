from django.urls import path
from . import views

urlpatterns = [
    path('', views.data_assets_list, name='data_assets_list'),
    path('login/', views.login_view, name='login'),
	path('logout/', views.logout_view, name='logout'),
    path('<int:pk>/', views.data_asset_detail, name='data_asset_detail'),
    path('search/', views.data_asset_search, name='data_asset_search'),
    path('data_assets/names/', views.data_asset_names, name='data_asset_names'),
    path('neural_search/', views.neural_search, name='neural_search'),
    path('query_data/', views.query_data_search, name='query_data_search'),
    path('query_data/<str:table_name>/', views.query_data, name='query_data'),
]
