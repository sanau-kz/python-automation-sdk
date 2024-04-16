from .database.DB import *
from .classes.DatabaseCredentials import DatabaseCredentials
from .classes.ApiCredentials import ApiCredentials

from .controllers.JobsController import JobsController

from datetime import datetime
import time


class Worker:

    def __init__(self, database_credentials: DatabaseCredentials, api_credentials: ApiCredentials):
        self.db = DB(
            database_credentials.name,
            user=database_credentials.user,
            password=database_credentials.password,
            host=database_credentials.host,
            port=database_credentials.port
        ).db

        self.jobs_controller = JobsController(self.db)

    def run(self):
        while True:
            time.sleep(40) if ((8 <= datetime.now().hour <= 20)
                               and (0 <= datetime.today().weekday() < 5)) else time.sleep(2)
            self.fetch_and_run_pending_job()

    def fetch_and_run_pending_job(self):
        # Gets the most top pending job
        selected_job_id = self.jobs_controller.get_last_job_id()

        if selected_job_id is None:
            return False
        job = self.jobs_controller.get_or_none(id=selected_job_id)

        # Checks if the job is already running
        if not self.jobs_controller.check_for_existing_job(job):
            return False

        # Checks if the job has required jobs
        if not self.jobs_controller.check_required_jobs(job):
            return False

        # Starts the job
        self.jobs_controller.execute_job(job)
