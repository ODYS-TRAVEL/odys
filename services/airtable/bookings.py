from .operations import Operations

class BookingTable(Operations):
    table_name = 'Bookings'

    def __init__(self, base):
        super().__init__(base)
