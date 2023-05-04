from pyairtable import Base


class AirtableBase:
    def __init__(self, api_key, base_id):
        self.api_key = api_key
        self.base_id = base_id
        self.base = Base(api_key, base_id)


class Operations(AirtableBase):
    def __init__(self, api_key, base_id):
        super().__init__(api_key, base_id)

    @property
    def table_name(self):
        raise NotImplementedError

    def operation(self, name, *args, **kwargs):
        return getattr(self.base, name)(self.table_name, *args, **kwargs)
