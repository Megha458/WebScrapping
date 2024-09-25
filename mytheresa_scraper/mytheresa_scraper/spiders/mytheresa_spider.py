import scrapy

class MytheresaSpider(scrapy.Spider):
    name = "mytheresa_spider"
    start_urls = ['https://www.mytheresa.com/int_en/men/shoes.html']

    def parse(self, response):
        # Extract product URLs from the page
        product_links = response.xpath('//a[@class="product-name"]/@href').getall()
        for link in product_links:
            yield scrapy.Request(url=link, callback=self.parse_product)

        # Follow pagination link to the next page
        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_product(self, response):
        yield {
            'breadcrumbs': response.xpath('//nav[@class="breadcrumb"]/a/text()').getall(),
            'image_url': response.xpath('//img[@id="product-image"]/@src').get(),
            'brand': response.xpath('//span[@class="designer-name"]/text()').get(),
            'product_name': response.xpath('//h1[@class="product-name"]/text()').get(),
            'listing_price': response.xpath('//span[@class="regular-price"]/text()').get(),
            'offer_price': response.xpath('//span[@class="special-price"]/text()').get(),
            'discount': response.xpath('//span[@class="discount"]/text()').get(),
            'product_id': response.xpath('//div[@class="product-id"]/text()').get(),
            'sizes': response.xpath('//ul[@class="sizes"]/li/text()').getall(),
            'description': response.xpath('//div[@class="description"]/p/text()').get(),
            'other_images': response.xpath('//div[@class="product-gallery"]//img/@src').getall()
        }
