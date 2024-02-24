from django.views import View
from django.shortcuts import render
import os
import pandas as pd

class QuantilesCalcView(View):
    template_name = 'QuantileCalc.html'

    def get(self, request, *args, **kwargs):
        ab_cir = float(request.GET.get('ab_cir', 0))
        pregnant_age = float(request.GET.get('pregnant_age', 0))
        selected_option = request.GET.get('options', '')
        excel_file_path = os.path.join('Quantiles', 'static', 'Quantiles', 'quantile_xl.csv')

        result = None
        mult = 1 if selected_option == 'by_day' else 7
        if ab_cir != 0:
            result = self.get_quantile_day(ab_cir, pregnant_age, excel_file_path, mult)
        # Pass the result to the template
        context = {'result': result}

        return render(request, self.template_name, context)

    def get_quantile_day(self, ab_cir, day, path, mult):
        if (day < 15 or day > 40) and (mult == 7):
            return "Please Provide a Week between 15 and 40"
        if (day < 105 or day > 280) and (mult == 1):
            return "Please Provide a day between 105 and 280"
        day_ = float(int(day * mult))
        df = pd.read_csv(path)
        df['day'] = df['pregweek'] * 7
        df.drop('median', inplace=True, axis=1)
        quantiles = df[df['day'] == day_]
        if ab_cir < quantiles['Q3'].iloc[0]:
            return "This baby's Abdominal circumference is lower than 97% of the babies"
        elif ab_cir < quantiles['Q5'].iloc[0]:
            return "This baby's Abdominal circumference is lower than 95% of the babies"
        elif ab_cir < quantiles['Q10'].iloc[0]:
            return "This baby's Abdominal circumference is lower than 90% of the babies"
        elif quantiles['Q95'].iloc[0] <= ab_cir < quantiles['Q97.5'].iloc[0]:
            return "This baby's Abdominal circumference is greater than  95% of the babies"
        elif ab_cir >= quantiles['Q97.5'].iloc[0]:
            return "This baby's Abdominal circumference is greater than  97.5% of the babies"
        else:
            return "This baby's result are Normal"
