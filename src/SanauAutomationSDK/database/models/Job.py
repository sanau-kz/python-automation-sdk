from playhouse.postgres_ext import *
from .BaseModel import BaseModel
from datetime import datetime,  timezone


class Job(BaseModel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        table_name = 'jobs'

    id = IntegerField(primary_key=True)
    database_id = IntegerField()
    name = CharField()
    task = CharField()
    status = CharField(default='pending')
    summary = JSONField(default={})
    params = JSONField(default={})
    log = TextField(default='')
    tries = IntegerField(default=0)
    related_jobs = JSONField(default={})
    priority = IntegerField(default=1)
    created_at = DateTimeField(default=datetime.now(timezone.utc))
    updated_at = DateTimeField(default=datetime.now(timezone.utc))
    started_at = DateTimeField(null=True)
    completed_at = DateTimeField(null=True)
    start_at = DateTimeField(null=True, default=datetime.now(timezone.utc))
