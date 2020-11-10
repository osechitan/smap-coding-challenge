from django.urls import path
from . import views

app_name = 'consumption'

urlpatterns = [
    path('', views.SummaryView.as_view(), name='summary'),
    path('summary/', views.SummaryView.as_view(), name='summary'),
    path('detail/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('summary/plot/', views.get_svg_summary, name='summary_plot'),
    path('detail/plot/<int:pk>/', views.get_svg_summary, name='detail_plot'),
]
