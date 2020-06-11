from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('sa', views.index, name='sa'),
    path('run', views.run, name="run"),
    path('run/<str:id>/', views.change_table, name="change_table"),
    path('', views.index, name="index"),
    path('run/<str:id>/execute', views.sa, name="sa")
]

