import jodel_api


class JodelCrawlAcc(jodel_api.JodelAccount):

    def __init__(self, city, lat, lng):
        super().__init__(city=city, lat=lat, lng=lng)
        self.city = city
