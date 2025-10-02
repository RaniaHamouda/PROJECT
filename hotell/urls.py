from django.urls import path
from . import views

# app_name = 'hotell'

urlpatterns = [
    path('hello/', views.HelloWord, name='hello'),
    # path('hotell/<int:hotell_id>', views.detail, name='detail'),
]