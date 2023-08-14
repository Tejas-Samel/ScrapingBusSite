# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SeatType(scrapy.Item):
    serviceKey = scrapy.Field()
    DOJ = scrapy.Field()
    SeatNumber = scrapy.Field()
    SeatStatus = scrapy.Field()
    seatprice = scrapy.Field()
    Discount_amount = scrapy.Field()
    Xcoordinate = scrapy.Field()
    Ycoordinate = scrapy.Field()
    Zcoordinate = scrapy.Field()
    height = scrapy.Field()
    width = scrapy.Field()
    timestamp = scrapy.Field()


class AbhibusItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    serviceKey = scrapy.Field()
    DOJ = scrapy.Field()
    operatorId = scrapy.Field()
    operatorName = scrapy.Field()
    DepartureTime =scrapy.Field()
    arriveTime = scrapy.Field()
    BusType =scrapy.Field()
    rating = scrapy.Field()
    rating_count =scrapy.Field()
    available_seats =scrapy.Field()
    is_sleeper = scrapy.Field()
    is_AC= scrapy.Field()
    seat = scrapy.Field()
    timestamp = scrapy.Field()

