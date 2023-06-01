from requests.exceptions import HTTPError


class Operations():
    '''
        https://pyairtable.readthedocs.io/en/latest/api.html
    '''
    def __init__(self, base):
        self.base = base

    @property
    def table_name(self):
        raise NotImplementedError

    def operation(self, name, *args, **kwargs):
        return getattr(self.base, name)(self.table_name, *args, **kwargs)
