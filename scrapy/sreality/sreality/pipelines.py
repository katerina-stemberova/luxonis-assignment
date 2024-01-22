# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import psycopg2
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SrealityPipeline:
    def process_item(self, item, spider):
        return item


class SaveToPostgresPipeline:
    def __init__(self):
        # connection details
        hostname = 'postgres'   # service name as defined in docker-compose.yml
        username = 'scrapy'
        password = 'scrapy'
        database = 'template1'

        # connect to the database
        try:
            self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        except Exception as e:
            print("ERROR: unable to connect to the database!")
            print(e)
        
        # create cursor, used to execute commands
        self.cur = self.connection.cursor()
        
        try:
            # create the table if it doesn't exist
            self.cur.execute("""
            CREATE TABLE IF NOT EXISTS sreality (
                id serial PRIMARY KEY, 
                title text,
                url VARCHAR(255)
            )
            """)
        except Exception as e:
            print("ERROR: unable to create 'sreality' table!")
            print(e)


    def process_item(self, item, spider):
        try:
            # define an insert statement
            self.cur.execute(""" INSERT INTO sreality (
                title, 
                url
                ) values (
                    %s,
                    %s
                    )""", (
                item["title"],
                item["url"])
            )

            # execute insert of data into the DB
            self.connection.commit()
            print("INFO: Inserted into DB:", item["title"], ",", item["url"])
        
        except Exception as e:
            print("ERROR: inserting an item into the 'sreality' table failed!")
            print(e)
    
        return item
    

    def close_spider(self, spider):
        # close cursor & connection to the DB 
        self.cur.close()
        self.connection.close()
        