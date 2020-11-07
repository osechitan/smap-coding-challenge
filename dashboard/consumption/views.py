# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import io
from PIL import Image
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
            'consumption_count': Consumption.objects.count()
        })
        return context


class DetailView(generic.DetailView):
    model = User
    template_name = 'consumption/detail.html'


def get_svg_summary(request):
    setPlt()
    svg = pltTosvg()
    plt.cla()
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response


def setPlt():
    consumption = Consumption.objects.annotate(month=TruncMonth('datetime'))\
                                               .values('month')\
                                               .annotate(consumption=Sum('consumption'))\
                                               .order_by('month')
    x = np.array([data['month'] for data in consumption])
    y = np.array([data['consumption'] for data in consumption])
    plt.plot(x, y, color='#00d5ff')
    plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    plt.title('Total amount of consumption', color='#3407ba')
    plt.xlabel('month')
    plt.ylabel('amount')


def pltTosvg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s
