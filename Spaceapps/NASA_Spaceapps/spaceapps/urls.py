from django.urls import path
from . import views



urlpatterns = [
    path('', views.HomePage.as_view(), name="home"),
    path('occurence/', views.OccurencePage.as_view(), name="occurence"),
    path('hazard/', views.HazardPage.as_view(), name="hazard"),
    path('report/', views.ReportPage.as_view(), name="report"),

]
