from Base import Base
import requests
import urllib.request
import config as cfg
import json


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
    def get_databases(self, headers):
        return requests.get(url=cfg.ONE_S_DATABASES, headers=headers).json()

    @catch
    def get_arm_employees(self, db_name, headers):
        return requests.get(url=cfg.ARM_EMPLOYEES.format(db_name=db_name), headers=headers).json()

    @catch
    def get_file_vault_file(self, params, headers):
        return requests.get(url=cfg.FILE_VAULT_DOWNLOAD_FILE, params=params, headers=headers)

    @catch
    def get_currency_rates(self, currency_date):
        return urllib.request.urlopen(url=cfg.CURRENCY_RATES.format(currency_date=currency_date))

    @catch
    def get_ogd_excel(self):
        return requests.get(url=cfg.OGD_EXCEL)

    @catch
    def get_domains(self, headers):
        return requests.get(url=cfg.DOMAINS, headers=headers).json()['domains']

    @catch
    def post_alerts(self, params, headers):
        return requests.post(url=cfg.ALERTS, params=params, headers=headers)

    @catch
    def post_taxation_organ(self, domain, out_dict, headers):
        return requests.post(url=cfg.FETCH_TAXATION_ORGANS.format(domain=domain),
                             data=json.dumps({'taxation_organs': out_dict}), headers=headers)

    @catch
    def resolve_alert(self, params, headers):
        return requests.put(url=cfg.RESOLVE_ALERT, params=params, headers=headers)

    @catch
    def resolve_all_alerts(self, entity_id, keys, headers):
        return requests.delete(url=cfg.RESOLVE_ALERT, json={'entity_id': entity_id, 'keys': keys}, headers=headers)
