from django.db import models
from django.utils import timezone
from datetime import timedelta


class Person(models.Model):
    Name = models.CharField(max_length=20, null=True)
    Address = models.CharField(max_length=200, null=True)
    Phonenumber = models.IntegerField(null=True , blank=True)
    email = models.EmailField(max_length=200, unique=True, null=True)
    def __str__(self):
        return self.email



class Table(models.Model):
    TYPE_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6')
    )
    table_type= models.CharField(max_length=200, null=True, choices=TYPE_CHOICES)
    person=models.ForeignKey(Person,null=True, on_delete=models.SET_NULL)
    price=models.CharField(max_length=10, null=True)
    start_time = models.DateTimeField(null=True, blank=True)
    accumulated_time = models.DurationField(default=timedelta)
    is_running = models.BooleanField(default=False)

    def start_stopwatch(self):
        if not self.is_running:
            self.start_time = timezone.now()
            self.is_running = True
            self.save()

    def stop_stopwatch(self):
        if self.is_running:
            elapsed_time = timezone.now() - self.start_time
            self.accumulated_time += elapsed_time
            self.is_running = False
            self.save()

    def reset_stopwatch(self):
        self.start_time = None
        self.accumulated_time = timedelta()
        self.is_running = False
        self.save()

    def get_elapsed_time(self):
        if self.is_running:
            elapsed_time = timezone.now() - self.start_time
            return self.accumulated_time + elapsed_time
        return self.accumulated_time
    

    def __str__(self):
        return self.table_type

    
