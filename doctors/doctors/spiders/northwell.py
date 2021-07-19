import scrapy


class NorthwellSpider(scrapy.Spider):
    name = 'northwell'
    allowed_domains = ['www.northwell.edu']
    start_urls = ['https://www.northwell.edu/physician-partners/doctors']

    def parse(self, response):
        profiles=response.css('.fad-profile-result')

        for profile in profiles:
            
            name=profile.css('.fad-profile-result__title-link ::text').get()
            #  ::text is a scrapy thing to get the text. Combining with putting a space 
            # tells css to do so for all descendants. No space is for that element
            raw_address=profile.css('.address__address ::text').getall()
            address=''
            for bit in raw_address:
                bit=bit.strip()
                if len(bit) > 0:
                    address = address + ' ' + bit
            # address=' '.join(address)
            phone=profile.css('.address__phone ::text').get()
            specialty=profile.css('.fad-profile-result__sub-title::text').get()

            yield {
                'name': name,
                'address':address.strip(),
                'phone': phone,
                'specialty': specialty,
            }

        next_page = response.css('a[aria-label="Next"]::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
# aria-label="Next"
# a[target="_blank"]