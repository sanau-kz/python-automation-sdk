from Base import Base
from Urls import Urls


class SanauAutomationSDK(Base):

    def __init__(self, region, domain):
        super().__init__(region, domain)
        self.urls = Urls(region, domain)
