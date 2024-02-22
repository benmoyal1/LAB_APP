
from django.urls import path,include
from .views import QuantilesCalcView
urlpatterns = [
    path('',QuantilesCalcView.as_view(),name='Quantiles')
]