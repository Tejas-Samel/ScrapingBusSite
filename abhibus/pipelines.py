# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class AbhibusPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()
    def create_connection(self):
        try:
            self.concn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='root',
            database = 'sciative_assignment_new',
            charset='utf-8',
            use_unicode=True
            )
            self.curr = self.conn.cursor()
        except Exception as ep:
            print(str(ep))

    def create_table(self):
        try:
            self.curr.execute("""CREATE TABLE route_new(
        routeid VARCHAR(15),
        DOJ VARCHAR(10) ,
        operatorId  VARCHAR(10),
        operatorName VARCHAR(50),
        DepartureTime VARCHAR(25),
        arriveTime VARCHAR(25),
        BusType VARCHAR(25),
        rating VARCHAR(5),
        rating_count FLOAT,
        is_sleeper BOOLEAN,
        is_AC BOOLEAN,
        available_seats VARCHAR(5),
        time_stamp TIMESTAMP,
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY 
        )""")

            self.curr.execute("""CREATE TABLE booking_new(
                routeid VARCHAR(11) ,
                DOJ VARCHAR(10) ,
                SeatNumber VARCHAR(10),
                SeatStatus VARCHAR(10),
                seatprice VARCHAR(10),
                Discount_amount VARCHAR(10),
                Xcoordinate VARCHAR(10),
                Ycoordinate VARCHAR(10),
                Zcoordinate VARCHAR(10),
                time_stamp TIMESTAMP,
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY
                )""")
            self.conn.commit()

        except Exception as epi:
            print(str(epi))




    def process_item(self, item, spider):
        self.store_in_db(item)
        return item

    def store_in_db(self,items):
        try:
            self.curr.execute(f"""
            INSERT INTO route_new(routeid,DOJ,operatorId,operatorName,DepartureTime,arriveTime,BusType,rating,
            rating_count,is_sleeper,is_AC,available_seats,time_stamp)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                              (items['serviceKey'].encode('utf-8'),items['DOJ'].encode('utf-8'),items['operatorId'].encode('utf-8'),
            items['operatorName'].encode('utf-8'),items['DepartureTime'].encode('utf-8'),items['arriveTime'].encode('utf-8'),
            items['BusType'].encode('utf-8'),items['rating'],items['rating_count'],
            items['is_sleeper'],items['is_AC'],items['available_seats'],items['timestamp']
            ))
            self.conn.commit()

            for i in items['seat']:
                if len(i) != 0:
                    self.curr.execute(f"""
                    INSERT INTO booking_new(routeid,DOJ,SeatNumber,SeatStatus,seatprice,
                    Discount_amount,Xcoordinate,Ycoordinate,Zcoordinate,time_stamp
                    ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                    """,(i['serviceKey'],i['DOJ'],i['SeatNumber'],
                         i['SeatStatus'],i['seatprice'],i['Discount_amount'],
                         i['Xcoordinate'],i['Ycoordinate'],i['Zcoordinate'],
                         items['timestamp']))

                    self.conn.commit()

        except Exception as ep:
            print(ep)
            exit()


