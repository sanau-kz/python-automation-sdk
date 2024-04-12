import time
from datetime import datetime
from .database.DB import *
from .database.models.Job import Job
from controllers.JobsController import JobsController


class Worker:

    def __init__(self, db_name, user, password, host, port):
        self.db = DB(db_name, user=user, password=password, host=host, port=port).db
        self.jobs_controller = JobsController(self.db)

    def run(self):
        while True:
            time.sleep(40) if ((8 <= datetime.now().hour <= 20)
                               and (0 <= datetime.today().weekday() < 5)) else time.sleep(2)
            self.fetch_and_run_pending_job()

    def fetch_and_run_pending_job(self):
        selected_job_id = self.jobs_controller.get_last_job_id()

        if selected_job_id is None:
            return False
        job = Job.get(selected_job_id)

        if not self.jobs_controller.check_required_jobs(job):
            return False

        if not self.jobs_controller.check_for_existing_job(job):
            return False

        self.jobs_controller.execute_job(job)
