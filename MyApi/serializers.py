from rest_framework import serializers
from .models import Person ,Table


class PersonaldataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Person
        fields='__all__'




class TableSerializer(serializers.ModelSerializer):
    persondetail = PersonaldataSerializer(read_only=True)
   
    class Meta:
        model=Table
        fields='__all__'



