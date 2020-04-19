from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path('', views.index, name='index'),
    path('mentions-legales/', views.legal, name='legal'),
    path('search/', views.search, name='search'),
    path('substitute/<str:product_id>/', views.product_detail, name='product_detail'),
    path('add_favorite/<str:product_id>/', views.add_favorite, name='add_favorite'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
]