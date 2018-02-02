from dress.vendor.workflow import *
from dress.helper import *

class CommandToShellScriptAction(Action):
    def run(self, *data):
        data = data[0]
        file_name = self.params['shell_script_file_name']
        with open(file_name, 'w') as f:
            f.write("#!/bin/sh -x\n")
            for line in data:
                f.write("%s\n" % (line))
        return file_name
