# to run 
# scrapy crawl tmdb_spider -o results.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/tv/66573-the-good-place']
    base_url = ['https://www.themoviedb.org']
    actors_list = [] 

    def parse(self, response):
        """
        Parsing method that navigates from the main movie/show page to
        the Cast & Crew page. Takes arguments self and a response object.
        Does not return any data.
        """
        # navigate to cast and crew page
        next_page = self.start_urls[0]+ "/cast"
        yield scrapy.Request(next_page, callback=self.parse_full_credits)

    def parse_full_credits(self, response):
        """
        Parsing method that navigates from the Cast & Crew page to
        individual pages for each actor in the show. Takes arguments
        self and a response object. Does not return any data.
        """

        actors = response.css("ol.people.credits a::attr(href)").getall()
          
        # list comprehension to get page links of actors only
        actors = [url for url in actors if url[:4] == "/per"]
        self.actors_list.extend(actors)
            
        # generator expression to navigate to actor pages
        yield from (scrapy.Request(self.base_url[0] + url, callback=self.parse_actor_page) for url in actors)

    def parse_actor_page(self, response):
        """
        Parsing method that yields a dictionary with two key-value pairs:
        actor for the actor name and movie_or_TV_name with the title
        of the shows or movies they have worked on from the actor's TMDB
        page.

        Takes arguments self and a response object.
        """
        # extract names and titles
        actor_name = response.css("h2.title a::text").get()
        movie_or_TV_shows = response.css("div.image img::attr(alt)").getall()

        # create a dict to store key-value pairs
        for movie_or_TV_name in movie_or_TV_shows:
            yield { "actor" : actor_name, 
                "movie_or_TV_name" : movie_or_TV_name}

