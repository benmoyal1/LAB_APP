from django.shortcuts import render
class QuantilesCalcView:
    def get(self,request,*args,**kwargs):
        return render(request,'QuantileCalc.html')