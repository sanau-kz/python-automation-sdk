from src.SanauAutomationSDK.api.Wrapper import Wrapper
from src.SanauAutomationSDK.api.models.Alert import Alert
from src.SanauAutomationSDK.utils.logutils import logger

import time


class AlertsHandler:

    def __init__(self, api_wrapper: Wrapper):
        self.api_wrapper = api_wrapper

    def resolve_all_alerts(self, entity_id, keys):
        return self.api_wrapper.resolve_all_alerts(entity_id=entity_id, keys=keys)

    def create_alert(self, alert: Alert, retries=0):
        alert.params.update(model_alert=alert.model_alert)
        try:
            return self.api_wrapper.post_alerts(params=alert.params)
        except Exception as e:
            logger.error(f'Failed to create alert: {e}')
            time.sleep(5)
            if retries < 10:
                return self.create_alert(alert, retries=retries + 1)
            else:
                raise e

    def resolve_alert(self, alert: Alert, retries=0):
        try:
            return self.api_wrapper.resolve_alert(params=alert.params)
        except Exception as e:
            logger.error(f'Failed to resolve alert: {e}')
            time.sleep(5)
            if retries < 10:
                return self.resolve_alert(alert, retries=retries + 1)
            else:
                raise e

    def get_alert(self, alert: Alert, retries=0):
        try:
            request = self.api_wrapper.get_alert(params=alert.params)
            if request is not None:
                return request.json()
            else:
                return None
        except Exception as e:
            time.sleep(1)
            if retries < 2:
                return self.get_alert(alert, retries=retries + 1)
            else:
                raise e
