from .BaseController import BaseController
from src.SanauAutomationSDK.database.models.Job import Job
from datetime import datetime, timezone
import json


class JobsController(BaseController):

    def __init__(self, db):
        super().__init__(db=db, model=Job(db=db))

    def start(self, process):
        self.create(
            status='started',
            log='',
            summary=json.dumps({}),
            started_at=datetime.now(timezone.utc))

    def update_summary(self, name, status, message):
        pass # TODO: сделать адейт саммари, поменять структуру джейсона если можно
