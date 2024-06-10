from rest_framework import serializers
from .models import *


class PersonaldataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Person
        fields='__all__'




class TableSerializer(serializers.ModelSerializer):
    person = PersonaldataSerializer(read_only=True)
    class Meta:
        model=Table
        fields='__all__'



