from django.urls import path
from django.contrib import admin
from app.views import trigger_task

urlpatterns = [
    path('admin/', admin.site.urls), 
    path("trigger-task/", trigger_task, name="trigger_task"),
]