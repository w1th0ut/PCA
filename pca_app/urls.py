from django.urls import path
from .views import pca_view

urlpatterns = [
    path('', pca_view, name='pca_view'),
]
