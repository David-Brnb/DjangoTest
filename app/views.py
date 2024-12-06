from django.http import JsonResponse
from .tasks import add

from datetime import datetime, timedelta

def trigger_task(request):
    result = add.apply_async(args=(1, 2), eta=datetime.utcnow()+timedelta(minutes=1))  # Call the task with arguments
    return JsonResponse({"task_id": result.id, "status": "Task triggered"})

def twenty_seconds():
    print("RUNNING EVERY TWENTY SECONDS")