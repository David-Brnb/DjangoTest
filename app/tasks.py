from __future__ import absolute_import, unicode_literals

from celery import shared_task

@shared_task
def add(x, y):
    return x + y


@shared_task
def twenty_seconds():
    print("This task runs every 20 seconds")
    return "Task completed"