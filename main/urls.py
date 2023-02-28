from django.urls import path
from main.views.main_views import get_report, trigger_report
from main.views.test_views import APIHealthCheck

urlpatterns = [
    path("health", APIHealthCheck.as_view(), name=APIHealthCheck.name),
    path("trigger_report", trigger_report, name="trigger_report"),
    path("get_report", get_report, name="get_report"),
]
