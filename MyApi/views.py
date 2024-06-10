from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError




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


        
    