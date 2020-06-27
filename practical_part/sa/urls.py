from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('sa', views.index, name='sa'),
    path('run', views.run, name="run"),
    path('run/<str:id>/', views.change_table, name="change_table"),
    path('', views.index, name="index"),
    path('run/<str:id>/<str:temp>/<str:r_rate>/<str:count>/<str:ci>/<str:sa>/execute', views.sa, name="sa"),
    path('results', views.show_results, name='results'),
    path('results/<str:id>/', views.filter_results, name="result_filter"),
    path('results/<str:id>/show', views.show_schedule, name="show")
]

