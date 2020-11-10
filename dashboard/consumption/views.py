# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import io
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter
from django.db.models import Sum
from django.views import generic
from .models import User, Consumption
from django.db.models.functions import TruncMonth
from django.http import HttpResponse


class SummaryView(generic.ListView):
    model = User
    context_object_name = 'user_list'
    queryset = User.objects.order_by('id')
    paginate_by = 20
    template_name = 'consumption/summary.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'consumption_count': get_consumption_count()
        })
        return context


class DetailView(generic.DetailView):
    model = User
    template_name = 'consumption/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('pk', '')
        context.update({
            # get count of consumption data
            'consumption_count': get_consumption_count(user_id)
        })
        return context


def get_consumption_count(user_id=None):
    count = 0
    if user_id is None:
        count = Consumption.objects.count()
    else:
        count = Consumption.objects.select_related('user')\
                                   .filter(user_id=user_id)\
                                   .count()
    return count


def get_svg_summary(request, pk=None):
    __setPlt(pk)
    svg = __pltTosvg()
    plt.cla()
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response


def __setPlt(pk):
    consumption_list = __get_consumption(pk)
    x = np.array([data['month'] for data in consumption_list])
    y = np.array([data['consumption'] for data in consumption_list])
    plt.plot(x, y, color='#00d5ff')
    plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    plt.title('Total amount of consumption', color='#3407ba')
    plt.xlabel('month')
    plt.ylabel('amount')


def __pltTosvg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s


def __get_consumption(pk=None):
    consumption_list = []
    if pk is None:
        consumption_list = Consumption.objects.annotate(month=TruncMonth('datetime'))\
                                              .values('month')\
                                              .annotate(consumption=Sum('consumption'))\
                                              .order_by('month')
    else:
        consumption_list = Consumption.objects.select_related('user')\
                                              .filter(user_id=pk)\
                                              .annotate(month=TruncMonth('datetime'))\
                                              .values('month')\
                                              .annotate(consumption=Sum('consumption'))\
                                              .order_by('month')
    return consumption_list
