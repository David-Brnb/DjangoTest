from django.urls import path
from django.contrib import admin
from app.views import trigger_task, trigger_twenty_seconds_task, start_thread, stop_thread

urlpatterns = [
    path('admin/', admin.site.urls), 
    path("trigger-task/", trigger_task, name="trigger_task"),
    path("trigger-task2/", trigger_twenty_seconds_task, name="trigger_twenty_seconds_task"),
    path("start-thread/", start_thread, name="start-thread"), 
    path("stop-thread/", stop_thread, name="stop-thread"), 
]