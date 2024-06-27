from django.db import models
from datetime import datetime
from django.utils import timezone

class Person(models.Model):
    Name = models.CharField(max_length=20, null=True,blank=True)
    Address = models.CharField(max_length=200, null=True,blank=True)
    Phonenumber = models.IntegerField(null=True , blank=True)
    email = models.EmailField(max_length=200, unique=True, null=True,blank=True)
    # tabletype=models.CharField(max_length=100, null=True, blank=True)
    tabletype=models.ForeignKey('Table',null=True, blank=True, on_delete=models.SET_NULL)
    frame=models.IntegerField(null=True , blank=True)
    def __str__(self):
        return str(self.email)

def get_current_time():
    return datetime.now().time()
class Table(models.Model):

    table_type= models.CharField(max_length=100, unique=True ,null=True)
    persondetail=models.ForeignKey(Person,null=True,  blank=True,on_delete=models.SET_NULL)
    rate=models.DecimalField(max_digits=7,decimal_places=2,default=0)
    price=models.DecimalField(max_digits=7,decimal_places=2,null=True , blank=True) 
    start_time = models.DateTimeField(null=True, blank=True)
    # time=models.DecimalField(max_digits=7,decimal_places=2,null=True , blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    frame_time_limit = models.TimeField(default=get_current_time)
    ac=models.BooleanField(default=False)
    button=models.BooleanField(default=False)
    inactive=models.BooleanField(default=False)
    is_running = models.BooleanField(default=False)


    def __str__(self):
        return str(self.table_type)

    
