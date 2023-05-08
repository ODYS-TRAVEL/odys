from .operations import Operations

class AgencyTable(Operations):
    table_name = 'Outgoing agencies'

    def __init__(self, base):
        super().__init__(base)
