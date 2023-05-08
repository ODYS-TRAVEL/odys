from pyairtable import Base
from .agencies import AgencyTable
from .clients import ClientTable
from .bookings import BookingTable

class AirtableBase:
    def __init__(self, api_key, base_id):
        self.api_key = api_key
        self.base_id = base_id
        self.base = Base(api_key, base_id)
        self.clients = ClientTable(self.base)
        self.agencies = AgencyTable(self.base)
        self.bookings = BookingTable(self.base)


