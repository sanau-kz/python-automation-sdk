from datetime import datetime, timezone


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
        result = self.model.raw(f"SELECT * FROM {self.model._meta.table_name} WHERE {'AND '.join([f'{k}=`{v}`' for k, v in kwargs.items()])} ORDER BY created_at DESC").execute()
        return result if result else None

    def create(self, **kwargs):
        return self.model.raw(f"INSERT INTO {self.model._meta.table_name} ({', '.join([k for k in kwargs.keys()])}) VALUES ({', '.join([v for v in kwargs.values()])})")

    def update(self, **kwargs):
        all_model_fields = (field for field in self.model._meta.fields)

        if 'id' not in kwargs:
            raise ValueError('id is required')

        for k, v in kwargs.items():
            if k not in all_model_fields:
                raise ValueError(f'{k} is not a valid field')

        item = self.get_by_id(kwargs['id'])
        fields_to_update = {attr_name: getattr(item, attr_name) for attr_name in item._meta.sorted_field_names}

        for k in kwargs.keys():
            fields_to_update[k] = kwargs[k]
        fields_to_update['updated_at'] = datetime.now(timezone.utc)

        return self.model.raw(f"UPDATE {self.model._meta.table_name} SET {', '.join([f'{k} = `{v}`' for k, v in fields_to_update.items()])} WHERE id = {kwargs['id']}").execute()

    def delete(self, item_id):
        self.model.raw(f"DELETE FROM {self.model._meta.table_name} WHERE id = {item_id}").execute()
