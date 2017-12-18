from task import Task
from dress.data.models import Host, Status

class CloneSiteTask(Task):
    source_host = None
    dest_host = None

    def __init__(self, source_host, dest_host):
        self.source_host = source_host
        self.dest_host = dest_host

    def run(self):
        pass
