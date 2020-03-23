from django.urls import path
from . import views
from .views import SavedListView

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('', views.home, name='home-home'),
    path('product/', views.product, name='home-product'),
    path('search/', views.search, name='home-search'),
    path('search-nova/', views.searchnova, name='home-search-nova'),
    path('proposition/', views.proposition, name='home-proposition'),
    path('saved/', SavedListView.as_view(), name='home-saved'),
    path('confirmation/', views.confirmation, name='home-confirmation'),
    path('infosaved/', views.infosaved, name='home-infosaved'),
    path('delete/', views.delete, name='home-delete'),
    path('validatedelete/', views.validatedelete, name='home-validatedelete'),
    path('mention/', views.mention, name='home-mention'),
    path('sentry-debug/', trigger_error),
]