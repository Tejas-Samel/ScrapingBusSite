from django.db import models

# Create your models here.
from turtle import width
from django.db import models


# Create your models here.
class Route_New(models.Model):
    class Meta:
        # managed = False
        db_table = "route_new"

    routeid = models.CharField(max_length=15)
    DOJ = models.CharField(max_length=10)

    operatorId = models.CharField(max_length=10)  # operator id
    operatorName = models.CharField(max_length=50)  # operator name
    DepartureTime = models.CharField(max_length=25)  # departure time
    arriveTime = models.CharField(max_length=25)  # arrival time
    BusType = models.CharField(max_length=25)
    rating = models.CharField(max_length=5)
    rating_count = models.CharField(max_length=20, null=True)
    is_sleeper = models.BooleanField(null=True)
    is_AC = models.BooleanField(null=True)
    available_seats = models.CharField(max_length=5)
    # time_stamp = models.DateTimeField()
    # id = models.AutoField(primary_key=True)

class Booking_New(models.Model):
    class Meta:
        # managed = False
        db_table = "booking_new"


    routeid = models.CharField(max_length=11)
    DOJ = models.CharField(max_length=10)  # date of journey
    SeatNumber = models.CharField(max_length=10)
    SeatStatus = models.CharField(max_length=10, blank=True)
    seatprice = models.CharField(max_length=10)
    Discount_amount = models.CharField(max_length=10)
    Xcoordinate = models.CharField(max_length=10, null=True)
    Ycoordinate = models.CharField(max_length=10, null=True)
    Zcoordinate = models.CharField(max_length=10, null=True)
    # time_stamp = models.DateTimeField()
    # id = models.AutoField(primary_key =True)
    # height = models.IntegerField(null=True)
    # width = models.IntegerField(null=True)