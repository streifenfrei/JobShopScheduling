from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('sa', views.index, name='sa'),
    path('test', views.test, name="test"),
    path('test/<str:id>/', views.change_table, name="change_table"),
    path('', views.index, name="index"),
    path('test/<str:id>/<str:temp>/<str:r_rate>/<str:count>/<str:ci>/<str:sa>/execute', views.sa, name="sa"),
    path('results', views.show_results, name='results'),
    path('results/<str:id>/', views.filter_results, name="result_filter"),
    path('results/<str:id>/show', views.show_schedule, name="show"),
    path('run', views.run, name="run"),
    path('run/<str:id>/', views.change_table, name="change_table"),
    path('run/<str:id>/sa', views.sa_final, name="sa_final"),
]

