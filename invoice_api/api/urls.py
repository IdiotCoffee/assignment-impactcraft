from django.urls import path
from .views import GenerateInvoiceView, AnalyzeInvoiceView

urlpatterns = [
    path('generate/', GenerateInvoiceView.as_view(), name="generate-invoice"),
    path('analyze/', AnalyzeInvoiceView.as_view(), name="analyze-invoice"),
]
