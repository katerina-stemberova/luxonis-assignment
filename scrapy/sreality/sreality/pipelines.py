# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SrealityPipeline:
    def process_item(self, item, spider):
        return item



import psycopg2

class SaveToPostgresPipeline:

    def __init__(self):
        ## Connection Details
        hostname = '0.0.0.0'
        username = 'scrapy'
        password = 'scrapy'
        database = 'template1'

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        
        ## Create the table if it doesn't exist
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS sreality (
            id serial PRIMARY KEY, 
            title text,
            url VARCHAR(255)
        )
        """)


    def process_item(self, item, spider):
        ## Define insert statement
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

        ## Execute insert of data into database
        self.connection.commit()
        print("~~Inserted into DB:", item["title"], ",", item["url"])
        return item
    

    def close_spider(self, spider):
        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()
        