from django.urls import path
from .views import ProtectedView, AdminOnlyView


urlpatterns = [
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('admin-only/', AdminOnlyView.as_view(), name='admin-only'),
]