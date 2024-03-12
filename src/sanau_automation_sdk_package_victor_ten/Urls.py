from Base import Base


class Urls(Base):

    def __init__(self, region, domain):
        super().__init__(region, domain)

    def get_region(self):
        print(self.region)

    def get_domain(self):
        print(self.domain)
