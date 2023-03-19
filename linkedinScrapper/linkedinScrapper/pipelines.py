# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import psycopg2
from itemadapter import ItemAdapter


class LinkedinscrapperPipeline:
    
    def __init__(self): #######

        ## Create/Connect to database
        self.connection = psycopg2.connect(host='localhost', user='postgres', password='Amine-1963', dbname='linkedin')
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Linkedin_jobs(
            job_title VARCHAR(255),
            job_detail_url text,
            job_listed VARCHAR(255),
            company_name VARCHAR(255),
            company_link text,
            company_location VARCHAR(255)
        )
        """)
    
    # def process_item(self, item, spider):
    #     return item

    def process_item(self, item, spider):

        ## Check to see if text is already in database 
        self.cur.execute("select * from Linkedin_jobs where job_detail_url = %s", (item['job_detail_url'],))
        result = self.cur.fetchone()

        ## If it is in DB, create log message
        if result:
            spider.logger.warn("Item already in database: %s" % item['job_detail_url'])


        ## If text isn't in the DB, insert data
        else:

            # Define insert statement
            self.cur.execute(""" insert into Linkedin_jobs(job_title, job_detail_url, job_listed, company_name, company_link, company_location) values (%s,%s,%s,%s,%s,%s)""", (
            str(item["job_title"]),
            str(item["job_detail_url"]),
            str(item["job_listed"]),
            str(item["company_name"]),
            str(item["company_link"]),
            str(item["company_location"])
            ))

            ## Execute insert of data into database
            self.connection.commit()
            return item 
    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()
