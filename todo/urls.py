from django.urls import path
from . import views

urlpatterns = [
    path('', views.database, name='index'),
    path('delete/<int:pk>/', views.delete_task, name='delete'),
    path('toggle/<int:pk>/', views.toggle_task, name='toggle'),
    path('edit/<int:pk>/', views.edit_task, name='edit'),
    path('register/', views.register, name='signup'),
]