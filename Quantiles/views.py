from django.shortcuts import render
from django.views import View

class QuantilesCalcView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'QuantileCalc.html')
