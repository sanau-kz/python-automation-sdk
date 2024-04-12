from .BaseController import BaseController
from ..database.models.Job import Job
from datetime import datetime, timezone
import json
import os


class JobsController(BaseController):

    def __init__(self, db):
        super().__init__(model=Job(db=db))

    def execute_job(self, job):
        try:
            # TODO Сделать логгер
            # logger.info(f'Starting job {job.id} - {job.task}! Wish me luck!')
            job.status = 'started'
            job.summary = '{}'
            job.started_at = datetime.now(timezone.utc)
            job.tries += 1
            job.save()

            # execute(job)

            job.completed_at = datetime.utcnow()
            job.status = 'completed'
            # TODO Сделать логгер
            # logger.info(f'Job {job.id} - {job.task} completed!')

        except Exception as e:
            # TODO Сделать логгер
            # logger.info(f'Ehhhh! {e}')
            self.update_summary(job_id=job.id, name='Ошибка!', status='failed', message=str(e))

            if (7 <= datetime.now().hour <= 18) or job.tries >= 10:
                # TODO Сделать логгер
                # logger.info(f'Im done :(')
                job.status = 'failed'
                job.completed_at = datetime.utcnow()
            else:
                # TODO Сделать логгер
                # logger.info(f'I will try again later!')
                job.status = 'pending'
            job.save()

        finally:
            self.check_last_job(job)

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

        job = self.get_or_none(database_id=database_id, task=task, status=['pending', 'started'])
        if job is None:
            job = self.create(name=name, task=task, status='pending', database_id=database_id, params=params, priority=priority, related_jobs=related_jobs)
        else:
            job = self.update(id=job[0].id, status='pending')

        return job

    def update_summary(self, job_id, name, status, message):
        job = self.get_or_none(id=job_id)
        job_summary = job.summary
        summary_steps = job_summary.setdefault('steps', [])
        if len(summary_steps) == 0 or summary_steps[-1]['name'] != name:
            summary_steps.append({'name': name, 'status': status, 'log': [str(datetime.now(timezone.utc)) + ' ' + message]})
        else:
            summary_steps[-1]['status'] = status
            summary_steps[-1]['log'].append(str(datetime.now(timezone.utc)) + ' ' + message)

        summary = json.dumps(job_summary, ensure_ascii=False)
        self.update(id=job_id, summary=summary)

    def get_last_job_id(self):
        query = self.get_or_none(status='pending', sorting_policy=('priority', 'asc'))
        selected_job_id = None
        if query.exists():
            for job in query:
                if self.get_or_none(status=['pending', 'started'],
                                    database_id=job.database_id,
                                    priority=('<', job.priority),
                                    created_at=('DATE', job.created_at.date())):
                    continue
                selected_job_id = job.id
                break
        return selected_job_id if selected_job_id is not None else None

    def check_required_jobs(self, job):
        required_jobs = job.related_jobs['required_jobs'] if 'required_jobs' in job.related_jobs.keys() else []

        related_jobs = self.get_all(status='failed',
                                    database_id=job.database_id,
                                    task=('IN', required_jobs),
                                    created_at=('DATE', job.created_at))
        if len(related_jobs) > 0:
            name = 'Пропуск'
            status = 'failed'
            message = f"Не были выполнены обязательные джобы ({', '.join(job.name for job in related_jobs)})."
            self.update_summary(job_id=job.id, name=name, status=status, message=message, )
            self.check_last_job(job)
            return False
        return True

    def check_for_existing_job(self, job_id):
        start = self.update(id=job_id,
                            status='started',
                            _where={'status': 'pending'},
                            )
        if not start:
            return False
        return True

    def check_last_job(self, job):
        try:
            unfinished_jobs = self.model.get_all(status='pending',
                                                 database_id=job.database_id,
                                                 created_at=('DATE', job.created_at.date()))
            if len(unfinished_jobs) > 0:
                return False
        except self.model.DoesNotExist:
            failed_jobs_names = [_.name for _ in self.model.get_all(status='failed',
                                                                    database_id=job.database_id,
                                                                    created_at=('DATE', job.created_at.date()))]
            if job.status == 'failed':
                failed_jobs_names.append(job.name)
            if len(failed_jobs_names) > 0:
                message = ', '.join(failed_jobs_names)
                print(f"Не прошли следующие проверки: {message}")
                return True
                # TODO Сделать алерт
                # get_db(job.database_id).set_alert(key="ones:database:validation:not_successful_alerts",
                #                                   message=f"Не прошли следующие проверки: {message}",
                #                                   severity=200)
            else:
                print("Все проверки прошли успешно!")
                return True
                # TODO Сделать резолв алерта
                # get_db(job.database_id).resolve_alert(key="ones:database:validation:not_successful_alerts")
        finally:
            if len(self.model.get_all(status='completed',
                                      database_id=job.database_id,
                                      created_at=('DATE', job.created_at.date()))) == 0:
                print("Начало дня!")
                # TODO Сделать резолв алерта
                # get_db(job.database_id).resolve_alert(key="ones:database:validation:not_successful_alerts")
