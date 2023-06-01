from .operations import Operations

class DMCSTable(Operations):
    '''
        Destinations Management Companies
    '''
    table_name = 'DMCs'

    def __init__(self, base):
        super().__init__(base)
