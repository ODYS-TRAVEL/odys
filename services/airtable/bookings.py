from .base import Operations

class BookingsTable(Operations):
    table_name = 'Bookings'

    def __init__(self, api_key, base_id):
        super().__init__(api_key, base_id)
