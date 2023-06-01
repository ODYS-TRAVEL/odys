from .operations import Operations

class ProjectsTable(Operations):
    table_name = 'Projects'

    def __init__(self, base):
        super().__init__(base)
