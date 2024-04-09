from .BaseController import BaseController
from src.SanauAutomationSDK.database.models.Job import Job
from datetime import datetime, timezone
import json
import os


class JobsController(BaseController):

    def __init__(self, db):
        super().__init__(model=Job(db=db))

    def start(self, job_id):
        self.update(
            id=job_id,
            status='started',
            log='',
            summary=json.dumps({}),
            started_at=datetime.now(timezone.utc))

    def enqueue(self, database_id, name, task, params=None, priority=None):
        script_dir = os.path.dirname(__file__)
        relative_path = os.path.join(script_dir, '../storage/job_relations.json')
        with open(relative_path, 'r') as file:
            job_relations = json.load(file)

        if params is None: params = {}
        if priority is None: priority = 2
        if task in job_relations.keys():
            related_jobs = dict()
            related_jobs['required_jobs'] = job_relations[task]
        else:
            related_jobs = {}

        job = self.get_by(database_id=database_id, task=task, status=['pending', 'started'])
        if job is None:
            job = self.create(name=name, task=task, status='pending', database_id=database_id, params=params, priority=priority, related_jobs=related_jobs)
        else:
            job = self.update(id=job[0].id, status='pending')

        return job

    def update_summary(self, job_id, name, status, message):
        job = self.get_by_id(job_id)

        job_summary = job.summary

        summary_steps = job_summary.setdefault('steps', [])
        if len(summary_steps) == 0 or summary_steps[-1]['name'] != name:
            summary_steps.append({'name': name, 'status': status, 'log': [str(datetime.now(timezone.utc)) + ' ' + message]})
        else:
            summary_steps[-1]['status'] = status
            summary_steps[-1]['log'].append(str(datetime.now(timezone.utc)) + ' ' + message)

        summary = json.dumps(job_summary, ensure_ascii=False)
        updated_at = datetime.now(timezone.utc)
        self.update(id=job_id, summary=summary, updated_at=updated_at)
