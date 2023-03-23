import scrapy
import json
import csv
from linkedinScrapper.items import LinkedinscrapperItem


class LinkedJobsSpider(scrapy.Spider):
    
   
    name = "linkedin_jobs"
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=data+science+intern&location=France&geoId=105015875&trk=public_jobs_jobs-search-bar_search-submit&start=' 
    custom_settings = {
        'DOWNLOAD_DELAY': 3 # 2 seconds of delay
        }
    
    def start_requests(self):
        first_job_on_page = 0
        first_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=first_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})
            
    def parse_job(self, response):
        first_job_on_page = response.meta['first_job_on_page']

        job_item = {}
        jobs = response.css('div.base-card')

        num_jobs_returned = len(jobs)
        print("******* Num Jobs Returned *******")
        print(num_jobs_returned)
        print('*****')
        for job in jobs:
            try:
                job_item['job_title'] = job.css("h3.base-search-card__title::text").get(default='not-found').strip()
            except:
                job_item['job_title'] = "Unknown"
 
            try:
                job_item['job_detail_url'] = job.css("a.base-card__full-link::attr(href)").get(default='not-found').strip()
            except:
                job_item['job_detail_url'] = "Unknown"

            try:
                job_item['job_listed'] = job.css('time.job-search-card__listdate::text').get(default='not-found').strip()
            except:
                job_item['job_listed'] = "Unknown"

            try:
                job_item['company_name'] = job.css('h4 a.hidden-nested-link::text').get(default='not-found').strip()
            except:
                job_item['company_name'] = "Unknown"

            try:
                job_item['company_link'] = job.css('h4 a.hidden-nested-link::attr(href)').get(default='not-found')
            except:
                job_item['company_link'] = "Unknown"
                
            try:
                job_item['company_location'] = job.css('span.job-search-card__location::text').get(default='not-found').strip()
            except:
                job_item['company_location'] = "Unknown"

            yield scrapy.Request(url=job_item['job_detail_url'], callback=self.parse_job_detail, meta={'job_item': job_item})
            
        
        if num_jobs_returned > 0:
            first_job_on_page = int(first_job_on_page) + 25
            next_url = self.api_url + str(first_job_on_page)
            yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})

    def save_record_to_file(self, record, filename):
            filename += ".json"
            with open(filename, 'a') as f:
                json.dump(record, f)
                f.write(',\n')
                
    def parse_job_detail(self, response):
        job_item = response.meta['job_item']
        # Extract data from the detail page
        try:
            job_item['description'] = ",".join(response.css("div.show-more-less-html__markup::text").getall())
        except:
            job_item['description'] = "Unknown"

        yield job_item


        
            
        # momemnt et vraismenlance 
        # acp clus et arbre 
        # tp : importance des variable
        # melange des lois 
        # variable latente - > distribution
        # ecriture de la densite . maximer la vraisemblance