from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView
from datetime import timedelta, datetime
from .models import Route_New, Booking_New
import json
from django.core import serializers
from django.db.models import Count

# Create your views here.
class homepage(TemplateView):

    def get(self,request):
        return render(request=request, template_name="homepage.html", context={})

    def post(self,request):
        Source = request.POST['Source']
        Destination = request.POST['Destination']
        routeid = request.POST['route_id']
        doj= request.POST['doj']

        abhibus_bus_info= Route_New.objects.filter(routeid=routeid)
        seat_info = Booking_New.objects.filter(routeid=routeid)

        bus_info = json.loads(serializers.serialize('json', abhibus_bus_info))
        seat_info = json.loads(serializers.serialize('json',seat_info))

        # print(type(bus_info[0]['fields']['available_seats']))
        # 1191528378 1203026991 1216821833

        try: SoldSeats = abs(len(seat_info) - int(bus_info[0]['fields']['available_seats']))
        except: SoldSeats = 0
        avg_booking = sum([int(i['fields']['seatprice']) for i in seat_info])/len(seat_info) if len(seat_info) else 0
        print(avg_booking)
        content = {
            'Source':str(Source).capitalize(),
            'Destination':str(Destination).capitalize(),
            'doj':doj,
            'SoldSeats':SoldSeats,
            'bus_info': bus_info,
            'pk':routeid,
            'avg_booking' : avg_booking,
            'TotalSeats' : len(seat_info),
            'data': seat_info
        }
        return render(request=request, template_name="homepage.html", context=content)












class info(TemplateView):
    def get(self,request,routeid,doj):

        abhibus_bus_info= Route_New.objects.filter(routeid=routeid)
        abhibus_bus_info = serializers.serialize('json',abhibus_bus_info)
        # for i in range(len(abhibus_bus_info))

        seat_info = Booking_New.objects.raw('SELECT DISTINCT SeatNumber FROM sciative_assignment_new.route_new WHERE routeid="1196115283";')
        # seat_info= serializers.serialize('json', seat_info)
        print(type(seat_info))
        k= serializers.serialize('json',seat_info)
        print(k)
        print(abhibus_bus_info)
        print("***")

        return render(request=request, template_name="table.html")
