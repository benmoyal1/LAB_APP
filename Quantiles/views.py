from django.views import View
from django.shortcuts import render
import os
import pandas as pd
import numpy as np
from scipy.stats import norm


class QuantilesCalcView(View):
    template_name = 'QuantileCalc.html'

    def get(self, request, *args, **kwargs):
        '''
        ab_cir =
        age =
        mean Reg(week) - Y ~ -4.5837 + 1.84235 * x + 0.40206 * X ** 2 + 0.00581 * x ** 3
        sd reg(week) - Y ~  1.4347 + 0.3996 * X
        qnorm(ab_cir,sd_reg,mean_reg)
        result = norm.ppf(ab_cir, loc=mean_reg, scale=sd_reg)
        caculate the quantile mean
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        ab_cir = float(request.GET.get('ab_cir', 0))
        pregnant_age = float(request.GET.get('pregnant_age', 0))
        selected_option = request.GET.get('options', '')
        mother_age = float(request.GET.get('mother_age', 0))
        births_num = int(request.GET.get('num_births', 0))

        if selected_option == 'by_day':
            pregnant_age /= 7

        mean_ = round(self.mean_poly(pregnant_age), 2)  # 340.6
        sd_ = round(self.sd_poly(pregnant_age), 2)  # 17.
        result = None
        if ab_cir != 0:
            result = round(norm.cdf(ab_cir, loc=mean_, scale=sd_), 2)
        mother_age_warning = True if mother_age >= 40 else False
        too_much_babies = True if births_num >= 7 else False
        context = {'result': result,
                   'Mother_age_suck_warning': mother_age_warning,
                   'too_much_babies_warning': too_much_babies}

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
        print("day is ", day_)
        print(df)
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

    def mean_poly(self, week):
        mean_coefs = [-0.00581, 0.40206, 1.84235, -4.5837]  # 0.0058X^3
        result = mean_coefs[0] * (week ** 3) + mean_coefs[1] * (week ** 2) + \
                 mean_coefs[2] * week + mean_coefs[3]
        return result

    def sd_poly(self, week):
        sd_coefs = [1.4347, 0.3996]  # 1.434X + 0.3996
        result = sd_coefs[1] * week + sd_coefs[0]
        return result
