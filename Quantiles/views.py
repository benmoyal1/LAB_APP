from django.views import View
from django.shortcuts import render


class QuantilesCalcView(View):
    template_name = 'QuantileCalc.html'

    def get(self, request, *args, **kwargs):
        # Get the numeric parameters from the URL
        param1 = float(request.GET.get('param1', 0))
        param2 = float(request.GET.get('param2', 0))

        # Perform the calculation (you can replace this with your actual calculation logic)
        result = param1 + param2

        # Pass the result to the template
        context = {'result': result}

        return render(request, self.template_name, context)
