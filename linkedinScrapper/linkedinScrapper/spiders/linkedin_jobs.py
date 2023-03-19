import scrapy
import json
import csv
from linkedinScrapper.items import LinkedinscrapperItem


class LinkedJobsSpider(scrapy.Spider):
    name = "linkedin_jobs"
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=data+science+intern&location=France&geoId=105015875&trk=public_jobs_jobs-search-bar_search-submit&start=' 

    def start_requests(self):
        first_job_on_page = 0
        first_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=first_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})

    def save_record_to_file(self, record, filename):
        filename += ".json"
        with open(filename, 'a') as f:
            json.dump(record, f)
            f.write(',\n')
            
    def to_csv(filename):
        with open(filename + '.json', 'r') as json_file:
            data = json.load(json_file)

        with open(filename+'.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)

            writer.writerow(data[0].keys())

            for row in data:
                writer.writerow(row.values())
            
    def parse_job(self, response):
        first_job_on_page = response.meta['first_job_on_page']

        job_item = {}
        jobs = response.css('div.base-card')

        num_jobs_returned = len(jobs)
        print("******* Num Jobs Returned *******")
        print(num_jobs_returned)
        print('*****')
        for job in jobs:
            
            job_item['job_title'] = job.css("h3.base-search-card__title::text").get(default='not-found').strip()
            job_item['job_detail_url'] = job.css("a.base-card__full-link::attr(href)").get(default='not-found').strip()
            job_item['job_listed'] = job.css('time.job-search-card__listdate::text').get(default='not-found').strip()

            job_item['company_name'] = job.css('h4 a.hidden-nested-link::text').get(default='not-found').strip()
            job_item['company_link'] = job.css('h4 a.hidden-nested-link::attr(href)').get(default='not-found')
            job_item['company_location'] = job.css('span.job-search-card__location::text').get(default='not-found').strip()
            self.save_record_to_file(job_item, "Linkedin_job_offers")

        
        if num_jobs_returned > 0:
            first_job_on_page = int(first_job_on_page) + 25
            next_url = self.api_url + str(first_job_on_page)
            yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})
            
        self.to_csv("Linkedin_job_offers")