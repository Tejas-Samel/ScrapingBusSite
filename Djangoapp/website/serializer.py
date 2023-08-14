from rest_framework import serializers
from .models import Route_New,Booking_New

class Route_New_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Route_New
        fields = '__all__'

class Booking_New_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Booking_New
        fields = '__all__'








