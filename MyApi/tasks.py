from celery import shared_task
from django.http import HttpResponse

@shared_task(bind=True)
def test_func(self):
    for i in range(10):
        print(i)
    return "done"

