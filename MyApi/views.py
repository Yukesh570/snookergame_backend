from django.shortcuts import render ,get_object_or_404
from .models import *
from .serializers import *
from django.utils.timezone import now
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from django.http import JsonResponse
import time
from decimal import Decimal



@api_view(['POST'])
def registerUser(request):
    data=request.data

    try:
        user= Person.objects.create(
            Name=data['Name'],
            Address=data['Address'],
            Phonenumber=data['Phonenumber'],
            email=data['email'],
        )
        serializer=PersonaldataSerializer(user,many=False)
        return Response(serializer.data)
    
    except IntegrityError:
        message={'detail':'User with this email already exists'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
def gettable(request,pk):
    table=Table.objects.get(id=pk)
    serializers=TableSerializer(table,many=False)
    return Response(serializers.data)


        
@api_view(['GET'])
def getalltable(request):
    table=Table.objects.all()
    serializers=TableSerializer(table,many=True)
    return Response(serializers.data)



def index(request):
    return render(request,'index.html')





def start_timer(request,pk):
    request.session['start_time'] = time.time()
    table =get_object_or_404(Table,pk=pk)
    table.start_time= timezone.now()
    table.time = 0
    table.is_running =True
    table.save()
    print('=====================================================stared',table.start_time)
    return JsonResponse({'status': 'Timer started'})


# def stop_timer(request,pk):
    
#     if 'start_time' in request.session:
#         start_time = request.session.pop('start_time')

#         elapsed_time = time.time() - start_time
#         table = get_object_or_404(Table, id=pk)  # Replace with the correct logic to identify the Table instance
#         table.is_running = False
#         table.time = Decimal(elapsed_time)
#         table.end_time= now()
#         table.price=(table.rate * table.time)/Decimal(60)
#         table.save()
#         return JsonResponse({'status': 'Timer stopped', 'elapsed_time': elapsed_time})
#     else:
#         return JsonResponse({'status': 'No timer started'})
    
        
def stop_timer(request,pk):
        table = get_object_or_404(Table, id=pk)  # Replace with the correct logic to identify the Table instance
        current_time = time.time()  # Get current time in seconds since the epoch
        elapsed_time = current_time - table.start_time.timestamp() 
        table.is_running = False
        table.time = Decimal(elapsed_time)
        table.end_time= now()
        table.price=(table.rate * table.time)/Decimal(60)
        table.save()
        return JsonResponse({'status': 'Timer stopped', 'elapsed_time': elapsed_time})

    
        