from playhouse.postgres_ext import *
from .BaseModel import BaseModel


class Database(BaseModel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        table_name = 'databases'

    id = IntegerField(primary_key=True)
    name = CharField()
    configuration = CharField()
    server = CharField()
    entity_id = IntegerField()
    sync_period = IntervalField()
