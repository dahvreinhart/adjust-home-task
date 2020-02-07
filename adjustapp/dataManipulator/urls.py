from django.conf.urls import url
from dataManipulator import views


urlpatterns = [
    url(r'^data$', views.DataPrintout.as_view()),
    url(r'^$', views.HomePageView.as_view()),
]