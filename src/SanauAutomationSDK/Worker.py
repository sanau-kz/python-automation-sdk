from .database.DB import DB
from .database.models.Job import Job
from .controllers.TestsController import TestsController
from datetime import datetime


class Worker:

    def __init__(self, db_name, user, password, host, port):
        self.db = DB(db_name, user=user, password=password, host=host, port=port).db

    def run(self):
        pass

    def fetch_tasks(self) -> Job:
        pass

