from Base import Base
from utils.decorators import catch
import requests
import config as cfg


class OGD(Base):

    def __init__(self, region, domain, access_key):
        super().__init__(region, domain, access_key)

    @catch
    def get_ogd_excel(self):
        return requests.get(url=cfg.OGD_EXCEL)
