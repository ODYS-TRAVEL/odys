from .base import Operations

class ClientsTable(Operations):
    table_name = 'Clients'

    def __init__(self, api_key, base_id):
        super().__init__(api_key, base_id)
