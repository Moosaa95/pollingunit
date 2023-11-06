# polling/urls.py
from django.urls import path
from .views import PollingUnitResultsView,WardDetailView, WardListView, GetWardsView, PollingUnitSearchView, LGASummedResultsView, EnterPollingUnitResultsView

app_name = 'pollingApp'

urlpatterns = [
    path('', PollingUnitSearchView.as_view(), name='polling_unit_search'),
    path('polling_unit/<int:polling_unit_id>/', PollingUnitResultsView.as_view(), name='polling_unit_results'),
    path('lga_summed_results/', LGASummedResultsView.as_view(), name='lga_summed_results'),
    path('enter_polling_unit_results/', EnterPollingUnitResultsView.as_view(), name='enter_polling_unit_results'),
     path('get_wards/', GetWardsView.as_view(), name='get_wards'),
     path('wards/', WardListView.as_view(), name='ward_list'),
     path('ward/<int:ward_id>/', WardDetailView.as_view(), name='ward_detail'),
]
