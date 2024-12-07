from django.http import JsonResponse
from .tasks import add
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json
import threading
import time

from datetime import datetime, timedelta

def trigger_task(request):
    result = add.apply_async(args=(1, 2), eta=datetime.utcnow()+timedelta(minutes=1))  # Call the task with arguments
    return JsonResponse({"task_id": result.id, "status": "Task triggered"})

def trigger_twenty_seconds_task(request):
    # Create or get the interval schedule
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=20,
        period=IntervalSchedule.SECONDS,  # Run every 20 seconds
    )

    # Create the periodic task
    task_name = "twenty_seconds_taskis"
    if not PeriodicTask.objects.filter(name=task_name).exists():
        PeriodicTask.objects.create(
            interval=schedule,
            name=task_name,
            task="app.tasks.twenty_seconds",  # Full path to the task
            args=json.dumps([]),  # Arguments for the task
        )
        return JsonResponse({"status": "Task scheduled"})
    else:
        return JsonResponse({"status": "Task already scheduled"})
    

# Store threads and their stop events
threads = {}

# Periodic task
def periodic_task(interval, stop_event):
    while not stop_event.is_set():
        print(f"Task executed")  # Replace with actual logic
        time.sleep(interval)

# View to start the thread
def start_thread(request):
    interval = int(request.GET.get("interval", 10))  # Seconds
    task_id = request.GET.get("task_id", "default_task")  # Unique identifier for the task

    # Check if the task already exists
    if task_id in threads:
        return JsonResponse({"status": "Task already running", "task_id": task_id})

    # Create a stop event
    stop_event = threading.Event()

    # Start a new thread
    task_thread = threading.Thread(target=periodic_task, args=(interval, stop_event))
    task_thread.daemon = True
    task_thread.start()

    # Save the thread and stop event
    threads[task_id] = stop_event

    return JsonResponse({"status": "Thread started", "task_id": task_id, "interval": f"{interval} seconds"})

# View to stop the thread
def stop_thread(request):
    task_id = request.GET.get("task_id", "default_task")  # Unique identifier for the task

    # Check if the task exists
    if task_id in threads:
        # Signal the thread to stop
        threads[task_id].set()

        # Remove the task from the dictionary
        del threads[task_id]

        return JsonResponse({"status": "Thread stopped", "task_id": task_id})
    else:
        return JsonResponse({"status": "Task not found", "task_id": task_id})