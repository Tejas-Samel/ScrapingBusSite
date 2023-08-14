from scrapy.utils.response import open_in_browser
import scrapy
import json
from datetime import datetime, timedelta
from ..items import AbhibusItem,SeatType


class AbhibusSpider(scrapy.Spider):
    name = 'mumbai'
    # Starting point
    start_urls = ['https://www.abhibus.com/bus_search/Mumbai/4/Pune/51/11-08-2022/O']
    seatlayout_url = 'https://www.abhibus.com/seatlayout'
    form_data = {"rid": "", "sourceid": "4", "destination": "51", "jdate": "", "concession": ""}

    def remove_non_ascii(self,text):
        return ''.join([i if ord(i) < 128 else ' ' for i in text])


    def parse(self, response):
        date_tobe_scraped='2022-08-11'

        request_main = \
            scrapy.http.Request(f'https://www.abhibus.com/getonewayservices/{date_tobe_scraped}/4/51',callback=self.api_parser)
        request_main.cb_kwargs['scrape_date'] = date_tobe_scraped
        yield request_main

    def api_parser(self, response, scrape_date):
        raw = json.loads(response.body.decode())
        service_list = raw['serviceDetailsList']
        for agent in service_list:
            rid = agent['serviceKey']
            self.form_data['rid'] = rid
            self.form_data['jdate'] = scrape_date

            agent_request = scrapy.http.FormRequest(self.seatlayout_url, callback=self.seat_layout_callback,
                                                    formdata=self.form_data)
            agent_request.cb_kwargs['scrape_date'] = scrape_date
            agent_request.cb_kwargs['rid'] = rid
            agent_request.cb_kwargs['bus'] = agent
            yield agent_request

    def seat_layout_callback(self, response, scrape_date, rid, bus):
        print(rid)
        list_seats = self.fare_processor(response,scrape_date,rid,bus)
        print(list_seats)
        abhibus_item = AbhibusItem()

        abhibus_item['serviceKey'] = bus['serviceKey']
        abhibus_item['DOJ'] = bus['journeyDate']
        abhibus_item['operatorId'] = bus['operatorId']
        abhibus_item['operatorName'] = bus['travelerAgentName']
        abhibus_item['DepartureTime'] = bus['startTime']
        abhibus_item['arriveTime'] = bus['arriveTime']
        abhibus_item['BusType'] = bus['busType']
        abhibus_item['rating'] = bus['rating']
        abhibus_item['rating_count'] = bus['noOfRatings']
        abhibus_item['is_sleeper'] = True if 'SLEEPER' in str(bus['busType']) else False
        abhibus_item['is_AC'] = True if 'AC' in str(bus['busType']) else False
        abhibus_item['seat'] = list_seats if not len(list_seats) == 0 else []
        abhibus_item['available_seats'] = bus['availableSeats']
        abhibus_item['timestamp'] = datetime.now()

        yield abhibus_item



    def fare_processor(self, response,bus_date,rid,bus):
        list_seats = []
        try:
            seat_fare = response.css('a.tooltip::attr(title)').extract()
            seat_availability = response.css('ul li.seat').extract()
            print(seat_availability)
            for seat in zip(seat_fare,seat_availability):
                seat_layout = SeatType()

                seat_layout['serviceKey'] = rid
                seat_layout['DOJ'] = bus_date
                seat_layout['SeatNumber'] = self.remove_non_ascii(seat[0].split('|')[0].split(':')[-1].strip())
                seat_layout['seatprice'] = seat[0].split('|')[-1].split(':',1)[-1].strip()
                seat_layout['SeatStatus'] = 'AV' if 'available' in seat[1] else 'BO'
                try:
                    seat_layout['Discount_amount'] = bus['offer_price']
                except:
                    seat_layout['Discount_amount'] = 'NULL'
                seat_layout['Xcoordinate'] = seat_layout['SeatNumber'][0]
                try:
                    seat_layout['Ycoordinate'] = seat_layout['SeatNumber'][1]
                except:
                    seat_layout['Ycoordinate'] = 'NULL'
                seat_layout['Zcoordinate'] = seat_layout['SeatNumber'][-1]
                seat_layout['timestamp'] = datetime.now()
                list_seats.append(seat_layout)
            return list_seats
        except Exception as e:
            print(str(e))


