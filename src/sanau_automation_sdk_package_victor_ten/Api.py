from Base import Base
import requests
import urllib.request
import config as cfg
import json
from utils.decorators import catch


class Api(Base):

    def __init__(self, region, domain, access_key):
        super().__init__(region, domain, access_key)

    @catch
    def get_databases(self, headers=None):
        if headers: headers = {**self.access_key, **headers}
        return requests.get(url=cfg.ONE_S_DATABASES.format(domain=self.domain), headers=headers).json()

    @catch
    def get_currency_rates(self, currency_date):
        return urllib.request.urlopen(url=cfg.CURRENCY_RATES.format(currency_date=currency_date))

    @catch
    def get_domains(self, headers=None):
        return requests.get(url=cfg.DOMAINS, headers=headers).json()['domains']
