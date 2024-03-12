from Base import Base
import requests
import config as cfg


def catch(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            return e
        return result

    return wrapper


class Urls(Base):

    def __init__(self, region, domain):
        super().__init__(region, domain)

    @catch
    def get_databases(self):
        pass    # TODO: requests.get()
