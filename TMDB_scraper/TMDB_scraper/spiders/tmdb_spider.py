# to run 
# scrapy crawl tmdb_spider -o results.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/tv/66573-the-good-place']
    base_url = ['https://www.themoviedb.org']

    def parse(self, response):
        """
        insert docstring
        """

        next_page = self.start_urls[0]+ "/cast"
        yield scrapy.Request(next_page, callback=self.parse_full_credits)

    def parse_full_credits(self, response):
        """
        insert docstring
        """
        actors = response.css("ol.people.credits a::attr(href)").getall()
        actors_list = []
        for url in actors:
            if url[:4] == "/per":
                actors_list.append(url)
                actors_url = self.base_url[0] + url
                actors_url = response.urljoin(actors_url)
                yield scrapy.Request(actors_url, callback=self.parse_actor_page)


    def parse_actor_page(self, response):
        """
        insert docstring
        """
        actor_name = response.css("h2.title a::text").get()
        movie_or_TV_shows = response.css("div.image img::attr(alt)").getall()

        for movie_or_TV_name in movie_or_TV_shows:
            yield { "actor" : actor_name, 
                "movie_or_TV_name" : movie_or_TV_name}
