# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.item import Item, Field

class LinkedinscrapperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_title = Field()
    job_detail_url = Field()
    job_listed = Field()
    company_name = Field()
    company_link = Field()
    company_location = Field()

