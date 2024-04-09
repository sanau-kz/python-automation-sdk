from datetime import datetime, timezone
import json


class BaseController:
    def __init__(self, model):
        self.model = model

    def get_by_id(self, item_id):
        result = self.model.raw(f"SELECT * FROM {self.model._meta.table_name} WHERE id = '{item_id}'").execute()
        return result[0] if result else None

    def get_by_name(self, item_name):
        if 'name' not in self.model._meta.fields:
            raise ValueError('name field is not defined')

        result = self.model.raw(f"SELECT * FROM {self.model._meta.table_name} WHERE name = '{item_name}'").execute()
        return result if result else None

    def get_by_created_at(self, item_created_at_date):
        result = self.model.raw(f"SELECT * FROM {self.model._meta.table_name} WHERE created_at = '{item_created_at_date}' ORDER BY created_at DESC").execute()
        return result if result else None

    def get_by_updated_at(self, item_updated_at_date):
        result = self.model.raw(f"SELECT * FROM {self.model._meta.table_name} WHERE updated_at = {item_updated_at_date} ORDER BY updated_at DESC").execute()
        return result if result else None

    def get_by(self, **kwargs):
        condition_text = ''
        for i, (k, v) in enumerate(kwargs.items()):
            if isinstance(v, list):
                condition_text += '( ' + 'OR '.join([f"{k}='{list_item}' " for list_item in v]) + ') '
            else:
                condition_text += f"{k}='{v}' "
            if len(kwargs.keys()) > i + 1:
                condition_text += 'AND '

        result = self.model.raw(f'''SELECT * FROM {self.model._meta.table_name} WHERE {condition_text} ORDER BY created_at DESC''').execute()
        return result if result else None

    def create(self, **kwargs):
        model_defaults = self.model._meta.defaults
        for k, v in model_defaults.items():
            if k.name == 'created_at' or k.name == 'updated_at':
                if k.name not in kwargs:
                    kwargs[k.name] = datetime.now(timezone.utc)
            else:
                if k.name not in kwargs:
                    kwargs[k.name] = v

        for k, v in kwargs.items():
            if isinstance(v, dict):
                kwargs[k] = json.dumps(v)
        # TODO: сделать возврат объекта модели после его создания
        return self.model.raw(f'''INSERT INTO {self.model._meta.table_name} ({", ".join([k for k in kwargs.keys()])}) VALUES ({", ".join([f"'{v}'" for v in kwargs.values()])})''').execute()

    def update(self, **kwargs):
        all_model_fields = [field for field in self.model._meta.fields]

        if 'id' not in kwargs:
            raise ValueError('id is required')

        for k, v in kwargs.items():
            if k not in all_model_fields:
                raise ValueError(f'{k} is not a valid field')
            if isinstance(v, dict):
                kwargs[k] = json.dumps(v)

        kwargs['updated_at'] = datetime.now(timezone.utc)

        self.model.raw(f'''UPDATE {self.model._meta.table_name} SET {", ".join([f"{k} = '{v}'" for k, v in kwargs.items()])} WHERE id = {kwargs['id']}''').execute()
        return self.get_by_id(kwargs['id'])

    def delete(self, item_id):
        self.model.raw(f"DELETE FROM {self.model._meta.table_name} WHERE id = {item_id}").execute()
