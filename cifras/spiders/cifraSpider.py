from scrapy import Spider
from scrapy.exceptions import CloseSpider
from slugify import slugify
import os


class CifraSpider(Spider):
    name = "cifras"

    def __init__(self, artist=None, **kwargs):
        if artist is None:
            print("********************************************")
            print("Defina o artista usando a opção -a")
            print(f"    scrapy crawl {self.name} -a artist=<artista>")
            print("********************************************")
            raise CloseSpider('Artista não fornecido')
        
        self.artist = artist
        self.slug_artist = slugify(artist)
        self.start_urls = [f'https://www.cifraclub.com.br/{self.slug_artist}']
        super().__init__(**kwargs)

    def parse(self, response):
        """Parse a página do artista"""
        music_list = response.css('#js-a-songs')
        if not music_list:
            music_list = response.css('#js-a-s-box')

        urls = music_list.css('a.art_music-link::attr(href)').getall()

        self.output_dir = os.path.join('output', self.slug_artist)
        if urls and not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir)

        for url in urls:
            yield response.follow(url, callback=self.parseMusicPage)


    def parseMusicPage(self, response):
        """Parse a página de cifra de uma música"""
        title = response.css('h1.t1::text').get()
        slug_title = slugify(title)

        tom_wrapper = response.css('#cifra_tom')
        if tom_wrapper:
            tom = [
                text.strip() for text in tom_wrapper.css('::text').getall()
            ]
            tom = ' '.join(tom)
        else:
            tom = ''

        capo_wrapper = response.css('#cifra_capo')
        if capo_wrapper:
            capo = [
                text.strip() for text in capo_wrapper.css('::text').getall()
            ]
            capo = ' '.join(capo)
        else:
            capo = ''

        cifra_container = response.css('pre')
        cifra = ''.join(cifra_container.css('::text').getall())

        with open(
            os.path.join(self.output_dir, slug_title + '.txt'), 'w'
        ) as f:
            f.write(title)
            f.write('\n')
            f.write(self.artist)
            
            if tom or capo:
                f.write('\n')
                f.write('\n')
                f.write(tom)
                f.write('\n')
                f.write(capo)
            
            f.write('\n')
            f.write('\n')
            f.write(cifra)
