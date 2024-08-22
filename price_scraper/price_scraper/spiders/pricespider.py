import scrapy
import json

class PricespiderSpider(scrapy.Spider):
    name = "pricespider"
    allowed_domains = ["www.rightmove.co.uk"]
    start_urls = ["https://www.rightmove.co.uk/house-prices/se1/southwark-bridge-road.html?page=1"]

    def parse(self, response):
       
        script_content =  response.xpath("//script[contains(text(), 'window.__PRELOADED_STATE__')]//text()").get()[29:]  

        data = json.loads(script_content) 

        properties = data['results']['properties']

        if len(properties) == 0:
            return None


        for property in properties:

            yield {
                'address': property['address'],
                'type': property['propertyType'],
                'transactions': property['transactions'],
                'locations': property['location'],
                'url': property['detailUrl']
                  
            }

        current_page = int(response.url.split('=')[-1])
       
        next_page = current_page + 1

        next_page_url = f"https://www.rightmove.co.uk/house-prices/se1/southwark-bridge-road.html?page={next_page}"  

        yield response.follow(next_page_url, callback = self.parse)  