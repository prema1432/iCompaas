"""
URL configuration for the v1 of the sanitized app.

The `urlpatterns` list routes URLs to views.
"""

from django.urls import path

from sanitized.views import SanitizedInputAPIView

app_name = 'sanitized'  # pylint: disable=C0103

urlpatterns = [
    path('sanitized/input/', SanitizedInputAPIView.as_view(), name='sanitized_input_v1'),
]
